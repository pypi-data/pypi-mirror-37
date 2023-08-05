# pylint: disable=C0103,R0902,W1202
"""
Module to generate data from arbitrary source modules as defined in config_io.
"""
import os
import sys
import time
import logging
import json
import threading
import six
from exoedge.namespaces import ChannelNamespace
from murano_client.client import WatchQueue
from exoedge.sources import ExoEdgeSource
from six.moves import queue
from exoedge import logger

path = os.path.dirname(
    os.path.realpath(__file__)
).rsplit('/', 1)[0] + '/exoedge/sources'
sys.path.append(path)

LOG = logger.getLogger(__name__)

class NeverEndingCallbacks(object):
    def __init__(self, callback, interval, function, args, kwargs):
        self.callback = callback
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.call_again()

    def call_again(self):
        LOG.critical("call_again: calling: {} with: {} and {}"
                     .format(self.function, self.args, self.kwargs))
        self.callback(self.function(*self.args, **self.kwargs))
        self.timer = threading.Timer(
            self.interval,
            self.call_again)
        self.timer.start()

    def start(self):
        LOG.info("starting timer...")
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

class Channel(ChannelNamespace, object):
    """
    A Channel is connected to a Source, which provides the Channel
    with data to send in data_in.

    This class provides methods to get new data from a source specified in
    config_io.
    """
    def __init__(self, **kwargs):
        """
        Channel initialized by config_io.ConfigIO._add_channel()

        Parameters:
        name:               The key used for the channel object in config_io
        display_name:       The human-readable display name of the Channel
        description:        The description of the Channel
        properties:         <<<General metadata store>>>
                            <<<TODO>>>
        protocol_config:    The configuration for the source protocol
        offset:             The `b` parameter in `y = mx + b` to be applied to
                            a value before being put in the Channel's queue
        multiplier:         The `m` parameter in `y = mx + b` to be applied to
                            a value before being put in the Channel's queue
        sample_rate:        The period in milliseconds between source samples,
                            minimum is 250
        report_rate:        The period in milliseconds between reports to
                            Murano, minimum is 250
        report_on_change:   Boolean to only send value if the value has changed
                            since last sample
        mode:               The mode with which the Source is run.
                            poll | async | async2
        down_sample:        Method by which to down sample values in Channel
                            queue
                            MAX | MIN | SUM | AVG | ACT
        async_timeout:      The timeout in seconds for waiting on the event
                            set by an `async`-mode source.
        app_specific_config The reference object to the source from which data
                            will be received
        """
        LOG.critical("Channel kwargs: {}".format(kwargs))
        ChannelNamespace.__init__(self, **kwargs)

        # DERIVED
        self.downsampler = DownSampler(self.protocol_config.down_sample) # pylint: disable=E1101
        self.async_timeout = kwargs.get('async_timeout', 1.0)
        self.last_value = None
        self.last_report = 0
        self.last_sample = 0
        self.q_out = queue.Queue() if self.protocol_config.down_sample else queue.LifoQueue()  # pylint: disable=E1101
        self.q_error_out = WatchQueue()
        self.source = None
        self.callback_timer = None

    def start_source(self):
        """ Get value from Source.

        Import Source module and run specified function, passing in
        Channel.source.parameters as keyword arguments.
        """
        LOG.critical("Starting source:: {}".format(dict(self)))

        if self.protocol_config.application.startswith(u'Modbus_'): # pylint: disable=E1101
            src = __import__('exoedge_modbus_tcp')
            self.source = src.ModbusExoEdgeSource()
            self.source.get_source()

        elif self.protocol_config.application == u'ExoSimulator': # pylint: disable=E1101
            src = __import__('exoedge.sources.exo_simulator')
            self.source = src.sources.exo_simulator.ExoSimulator()
            self.source.get_source()

        else:
            # classic style
            LOG.critical(
                "no supported source found. using generic module.function(*args, **kwargs) style.")
            src = __import__(self.protocol_config.app_specific_config['module']) # pylint: disable=E1101
            self.callback_timer = NeverEndingCallbacks(
                self.put_sample,
                self.protocol_config.sample_rate / 1000.0, # pylint: disable=E1101
                getattr(src, self.protocol_config.app_specific_config['function']), # pylint: disable=E1101
                self.protocol_config.app_specific_config['positionals'], # pylint: disable=E1101
                self.protocol_config.app_specific_config['parameters'] # pylint: disable=E1101
            )

        LOG.critical("Source started:: {}".format(src))

    def stop_source(self):
        LOG.warning("stopping source: {}".format(self))
        if isinstance(self.source, ExoEdgeSource):
            self.source.stop()
        elif self.callback_timer:
            self.callback_timer.cancel()
        else:
            LOG.critical("Don't know how to stop source: <({} ){}>"
                         .format(type(self.source), self.source))
        self.source = None

    def is_sample_time(self, blocking=False):
        """ Sleep for the sample rate

        # FEATURE_IMPLEMENTATION: sample_rate
        """
        sr = self.protocol_config.sample_rate / 1000.0 # pylint: disable=E1101
        if blocking:
            time.sleep(sr)
        diff = time.time() - self.last_sample
        is_sample_time = diff >= sr
        return is_sample_time

    def put_sample(self, sample):
        """ Place data in queue.

        In the future, this method will be switchable and optionally send
        data to gmq or SQL database, e.g. send_data_to_gmq(data)

        Parameters:
        sample:           Datapoint to be placed in queue.
        """
        LOG.info("putting sample: {}".format(sample))
        data = Data(
            sample,
            gain=self.protocol_config.multiplier, # pylint: disable=E1101
            offset=self.protocol_config.offset) # pylint: disable=E1101
        self.q_out.put(data)
        self.last_sample = data.ts

    def put_channel_error(self, error):
        LOG.info("putting error: {}".format(error))
        self.q_error_out.put(str(error))
        self.last_sample = time.time()

    def set_report_stats(self, last_value, last_report):
        self.last_value = last_value
        self.last_report = last_report

    def is_report_time(self):
        """ Determine whether or not to run emit()

        If the report_rate duration has passed, or report_on_change is
        set to True, call emit()
        """
        t = time.time()
        _t = self.last_report + self.protocol_config.report_rate / 1000.0 # pylint: disable=E1101
        if self.protocol_config.report_on_change or t >= _t: # pylint: disable=E1101
            return True
        return False


class Data(tuple):
    """ Class to attach a timestamp to new data that is generated """
    def __new__(cls, d, **kwargs):
        """ Subclasses tuple. (timestamp, data) """
        cls.ts = time.time()
        cls.offset = kwargs.get('offset')
        cls.gain = kwargs.get('gain')
        if not isinstance(d, bool):
            try:
                cls.d = d * cls.gain + cls.offset
            except TypeError:
                cls.d = d
            # Attempt to JSON serialize the data point. If not
            # serializable, force into string.
            try:
                LOG.debug("data (json): {}".format(json.dumps(cls.d)))
            except TypeError:
                cls.d = str(cls.d)
        else:
            # support bool-type data
            cls.d = d

        return tuple.__new__(Data, (cls.ts, cls.d))

    def age(self):
        """ Return age of data point in seconds """
        return time.time() - self.ts


class DownSampler(object):
    """ Class to deal with down sampling Channel data

    Methods:
    max:            Maximum value in list
    min:            Minimum value in list
    sum:            Sum of values in list
    avg:            Average of values in list
    act:            Last value in list ("actual value")
                    TODO: determine if this should return entire list
                          and if omitting down_sample in channel config
                          should result in the last value instead
    """
    method_mapper = {
        'max': max,
        'min': min,
        'sum': sum,
        'avg': lambda ls: float(sum(ls))/len(ls),
        'act': lambda ls: ls[-1]    # ls.pop()
    }

    def __init__(self, method):
        """
        Initialized by Channel.__init__()
        """
        self.method = method.lower()
        self._fn = self.method_mapper.get(self.method)

    def __repr__(self):
        return '<{}: {}>'.format(self.method, self._fn)

    def down_sample(self, data):
        """ Down sample data

        Assume data is list of tuples, e.g.
        [(ts, val), (ts, val), ...]
        """
        LOG.debug('Performing downsample %s on %s', self.method, data)
        try:
            return self._fn([d[1] for d in data])
        except:
            # kludge for non-tuple data
            return self._fn(data)
