"""
ExoEdge module. Provides high-level functionality to play nicely
with Exosite's Remote Condition Monitoring solution for Industrial IoT.
"""
# pylint: disable=W1202
from __future__ import print_function
import sys
import json
import logging
import threading
import time
import six
from exoedge.config_io import ConfigIO
from murano_client.client import StoppableThread, WatchQueue
from exoedge import logger
from six.moves import queue

PY_VERSION = sys.version_info[0]

LOG = logger.getLogger(__name__)


class ExoEdge(object):
    """
    ExoEdge is the root class for integration with ExoSense. An instance
    is created from a Device and is set up using one of several strategies:
        -   local:      Set up ExoEdge from a local file. Upon completion
                        write this value to Murano.
        -   remote:     Set up ExoEdge from config_io in Murano.
    TODO: GMQ support
    TODO: refactor to use q.put() and q.get()
    """

    def __init__(self,
                 D,
                 **kwargs):
        """ Onus of initialization is on the application.

        Parameters:
        D:                  Device/connection object from murano_client.
        strategy:           The strategy with which to instantiate an ExoSense
                            object.
                            local | read | subscribe
        config_io_file:     Local file used to cache copy of config_io.
                            Typically `./<UUID>.json`.
        cache_config_io:    Whether or not to save a local copy of
                            config_io in config_io_file.
        config_io_sync:     Whether or not to keep local copy of config_io
                            synced with Murano.
        """
        self.strategy = kwargs.get('strategy') or 'local'
        if self.strategy not in ['remote', 'local']:
            raise ExoEdgeException("Strategy {} not a valid option. Choose from 'remote', 'local'."
                                   .format(self.strategy))

        self.config_io = ConfigIO()
        self.device = D
        self.__is_stopped = False

        self.cache_config_io = not kwargs.get('no_config_cache')  # cache_config_io
        self.config_io_file = kwargs.get(
            'config_io_file') or '{}.json'.format(kwargs.get('murano_id'))
        self.config_io_sync = not kwargs.get('no_config_sync')    # config_io_sync

        if self.config_io_sync:
            self.config_io_watcher = ConfigIOWatcher(
                t_config_io=self.config_io,
                device=self.device,
                config_io_file=self.config_io_file,
                cache_config_io=self.cache_config_io)

        self.data_in_writer = DataInWriter(
            config_io=self.config_io,
            device=self.device)

        if kwargs.get('debug'):
            LOG.setLevel(getattr(logging, kwargs.get('debug').upper()))

    def stop(self):
        """ Stop reporting

        Calls config_io.ConfigIO.stop(), which eventually causes the Channels
        and their respective ChannelWatchers to stop gracefully.
        """
        LOG.info('stopping...')
        self.__is_stopped = True
        self.config_io.stop()

        if self.config_io_sync:
            self.config_io_watcher.stop()

        self.data_in_writer.stop()
        self.device.stop_all()

    def is_stopped(self):
        return self.__is_stopped

    def setup(self):
        self.device.start_client()
        if self.strategy == 'local':
            try:
                self.config_io.set_config_io(self.read_local_config_io())
                self.tell_mur_config_io()
            except NoLocalConfigIO:
                LOG.warning("No local config_io to load.")
        elif self.strategy == 'remote':
            self.retrieve_remote_config_io()
            self.write_local_config_io()

        _ = self.config_io_watcher.start() if self.config_io_sync else None
        self.config_io.start()

        self.data_in_writer.start()

    def tell_mur_config_io(self):
        """ Write to Murano config_io resource. """
        with self.config_io.l_new_config:
            self.device.tell(resource='config_io',
                             timestamp=time.time(),
                             payload=json.dumps(self.config_io._new_config_io)) # pylint: disable=W0212

    def write_local_config_io(self):
        """ Write config_io to local file.

        TODO: Rename method.
        """
        if self.cache_config_io:
            LOG.info('writing the following to local config io file %s:',
                     self.config_io_file)

            with self.config_io.l_new_config:
                LOG.info("Writing config to: {} ::\n{}"
                         .format(self.config_io_file,
                                 json.dumps(self.config_io._new_config_io, indent=2))) # pylint: disable=W0212

                with open(self.config_io_file, 'w') as __f:
                    json.dump(self.config_io._new_config_io, __f) # pylint: disable=W0212

    def read_local_config_io(self):
        """ Read config_io from local file. """
        infostr = 'READING LOCAL CONFIG_IO'
        LOG.critical('\n{:-^80}\n'.format(infostr))

        if self.config_io_file:
            try:
                return json.load(open(self.config_io_file, 'r'))

            except IOError:
                raise NoLocalConfigIO('config_io file {} does not exist.'
                                      .format(self.config_io_file))

        else:
            raise NoLocalConfigIO('A local config_io file has not been set.')

    def retrieve_remote_config_io(self):
        """ Get config_io from Murano """
        infostr = 'RETRIEVING CONFIG_IO FROM EXOSENSE'
        LOG.critical('\n{:-^80}\n'.format(infostr))

        inbound = self.device.watch(timeout=5.0)

        if inbound and inbound.resource == 'config_io':
            value = inbound.payload
            try:
                self.config_io.set_config_io(json.loads(value))
                self.tell_mur_config_io()

            except ValueError:
                LOG.critical('ERROR: `%s` is invalid JSON. config_io must be valid JSON', value)
        else:
            if not self.is_stopped():
                self.retrieve_remote_config_io()


class DataInWriter(StoppableThread, object):
    """ This class has two threads: DataInWriter and DataInWriter.DataWatcher.

    The DataInWriter thread simply uploads all data in its outbound queue to Exosense.

    The DataInWriter.DataWatcher thread process all channels for data and errors, then
    puts them into the DataInWriter outbound queue for uploading.
    """
    def __init__(self,
                 config_io=None,
                 device=None,
                 wait_timeout=1.0):
        """
        DataInWriter initialized by ExoEdge.go()

        Parameters:
        wait_timeout:       Timeout to wait for e_send_data_in event before
                            reevaluating own stop status
        """
        StoppableThread.__init__(self, name='DataInWriter')
        self.device = device
        self.t_config_io = config_io
        self.wait_timeout = wait_timeout
        self.q_outbound_data = WatchQueue()

    def channel_data_watcher(self):
        """ Process Channel queues for data and errors. This thread is
        responsible for all channel data getting into the outbound queue.
        """
        while True:
            data_in = {}
            __error = {'__error': []}
            for name, channel in self.t_config_io.channels.items():
                if not channel.q_out.empty():
                    # FEATURE_IMPLEMENTATION: report_rate
                    if channel.is_report_time():
                        downsampled = channel.downsampler.down_sample(
                            list(channel.q_out.queue))
                        # FEATURE_IMPLEMENTATION: report_on_change
                        if not channel.protocol_config.report_on_change:
                            data_in[name] = downsampled
                            channel.set_report_stats(downsampled, time.time())
                            try:
                                channel.q_out.queue.clear()
                            except AttributeError:  # LifoQueue.queue is a list
                                channel.q_out.queue = []
                        else:
                            if downsampled != channel.last_value:
                                data_in[name] = downsampled
                                channel.set_report_stats(downsampled, time.time())
                            try:
                                channel.q_out.queue.clear()
                            except AttributeError:  # LifoQueue.queue is a list
                                channel.q_out.queue = []
                while not channel.q_error_out.empty():
                    error = channel.q_error_out.safe_get(timeout=0.001)
                    if error:
                        __error['__error'].append({name: error})

            if data_in:
                self.q_outbound_data.put(data_in)
            if __error.get('__error'):
                self.q_outbound_data.put(__error)
            time.sleep(0.01)

    def run(self):
        """ Process the outbound queue that DataInWriter.DataWatcher
        fills with channel data and errors.
        """
        LOG.debug('starting')
        data_watcher = StoppableThread(
            name="DataInWriter.DataWatcher",
            target=self.channel_data_watcher
        )
        data_watcher.setDaemon(True)
        data_watcher.start()

        while not self.is_stopped():

            data = self.q_outbound_data.safe_get(timeout=5.0)

            if data:
                LOG.critical('WRITING DATA: %s', data)
                self.device.tell(resource='data_in',
                                 timestamp=time.time(),
                                 payload=json.dumps(data))
            else:
                LOG.debug('NO DATA TO SEND')

        LOG.debug('exiting')


class ConfigIOWatcher(StoppableThread, object):
    """
    Class to deal with keeping local and cloud config_io
    in sync. Created if config_io_sync is set to True
    upon initiation of ExoEdge.
    """
    def __init__(self,
                 t_config_io=None,
                 device=None,
                 config_io_file=None,
                 cache_config_io=False,
                 timeout=300000):
        """
        Initialized by ExoEdge.go()

        Parameters:
        config_io_file:     File to save local copy of config_io
        cache_config_io:    Whether or not to save a local copy of config_io
        timeout:            Timeout to longpoll config_io resource in Murano
        """
        StoppableThread.__init__(self, name="ConfigIOWatcher")
        self.setDaemon(True)

        self.t_config_io = t_config_io
        self.device = device
        self.cache_config_io = cache_config_io
        self.config_io_file = config_io_file
        self.timeout = timeout

    def write_local_config_io(self):
        """ Write config_io to local file.

        """
        with self.t_config_io.l_new_config:
            LOG.debug('writing to local config io file %s',
                      self.config_io_file)
            with open(self.config_io_file, 'w') as __f:
                json.dump(self.t_config_io._new_config_io, __f)

    def run(self):
        """ Longpoll config_io.

        Informs config_io.ConfigIO that new config_io has been found.
        """
        while not self.is_stopped():
            inbound = self.device.watch(timeout=5)
            if inbound and inbound.resource == 'config_io':
                try:
                    self.t_config_io.set_config_io(json.loads(inbound.payload))

                    self.device.tell(resource='config_io',
                                     payload=inbound.payload,
                                     timestamp=time.time())
                    _ = self.write_local_config_io() if self.cache_config_io else None

                except ValueError:
                    LOG.critical(
                        'ERROR: `{}` is invalid JSON. config_io must be valid JSON'
                        .format(inbound.payload))

            else:
                LOG.debug('No config_io payload')


class ExoEdgeException(Exception):
    """
    Base exception class
    """
    pass

class ConfigIONotFound(ExoEdgeException):
    pass

class NoLocalConfigIO(ConfigIONotFound):
    pass

