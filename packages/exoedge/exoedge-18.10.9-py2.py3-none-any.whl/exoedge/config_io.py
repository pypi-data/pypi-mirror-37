# pylint: disable=W0141,W0110,C0103,W1202
"""
ExoEdge ConfigIO module to handle Channel creation from a config_io object.
"""
from __future__ import print_function
import threading
import logging
import json
from exoedge.channel import Channel
from exoedge.sources import ExoEdgeSource
from murano_client.client import StoppableThread
from exoedge import logger

LOG = logger.getLogger(__name__)

class ConfigIO(StoppableThread, object):
    """
    This class provides methods to create channels from a
    config_io and to format the data_in object to be sent
    to Murano. ConfigIO must be supplied a config_io as a
    dictionary.
    """
    __lock = threading.Lock() # used by channelwatcher to set a config_io event
    e_send_data_in = threading.Event()
    e_new_config = threading.Event()
    l_new_config = threading.Lock()

    def __init__(self,
                 config_io=None,
                 wait_timeout=1.0):
        StoppableThread.__init__(self, name="ConfigIO")
        self.config_io = {}
        self.wait_timeout = wait_timeout
        with ConfigIO.l_new_config:
            self._new_config_io = config_io
        self.last_report = 0
        self.channels = {}

    def stop(self):
        """ Stop all activity.

        Stops activity of all Channel threads, Channel-
        Watcher threads, and the ConfigIO thread.
        """
        LOG.warning("Stopping ConfigIO...")
        self.stop_all_channels()
        super(ConfigIO, self).stop()

    def has_channels(self):
        """ Return whether or not ConfigIO has channels.

        Used to determine if there are channels to stop.
        """
        return bool(self.channels)

    def _add_channel(self, name, ch_cfg):
        """ Create Channel and ChannelWatcher threads.

        Create a Channel and ChannelWatcher from a channel
        configuration object. Store them in the ConfigIO.channels
        dictionary.

        Parameters:
        ch_cfg:     the object representation of the channel
                    taken from config_io.
        name:       the key of the ch_cfg object in config_io

        """
        LOG.info('adding channel %s', name)
        ch_cfg['name'] = name
        channel = Channel(**ch_cfg)

        self.channels[name] = channel
        return

    def stop_all_channels(self):
        """ Stop Channel threads.

        Call channel.stop() for all Channels in ConfigIO.channels.
        Called by ConfigIO.run() when a new config_io is received.
        """
        LOG.warning('stopping all channels')
        for _, channel in self.channels.items():
            LOG.warning("Stopping ExoEdgeSource: {}".format(channel))
            channel.stop_source()
        self.channels = {}

    def set_config_io(self, cfg):
        """ Handle a new config_io.

        Handler for storing a newly received config_io and
        notifying the thread accordingly. Called by
        exo_edge.ConfigIOWatcher.run()

        Parameters:
        cfg:        the object representation of the config_io
        """
        LOG.critical('Received new config_io:\n%s',
                     json.dumps(cfg, indent=2))
        with ConfigIO.l_new_config:
            self._new_config_io = cfg
        self.e_new_config.set()

    def run(self):
        """ Update ConfigIO and Channels upon new config_io.

        Waits for a new config_io event set by ConfigIO.set_config_io() and
        subsequently stops existing channels before creating new channels from
        the newly received config_io object. Starts Channels and ChannelWatchers.
        """
        LOG.debug('starting')
        self.e_new_config.set()     # set upon start()
        while not self.is_stopped():
            if self.e_new_config.wait(self.wait_timeout):
                with ConfigIO.l_new_config:
                    if self._new_config_io:
                        LOG.debug('Received config_io')

                        if self.has_channels():
                            self.stop_all_channels()

                        if 'channels' in self._new_config_io.keys():
                            for name, cfg in self._new_config_io['channels'].items():
                                self._add_channel(name, cfg)

                            # start all Channels and ChannelWatchers
                            for channel in self.channels.values():
                                LOG.critical("STARTING CHANNEL: {}".format(dict(channel)))
                                channel.start_source()

                        else:
                            LOG.critical('Received new config_io without channels.')
                    else:
                        LOG.info("No new config_io received.")
                self.e_new_config.clear()

                with ConfigIO.l_new_config:
                    self.config_io = self._new_config_io
            else:
                LOG.debug('no new config')
        LOG.debug('exiting')


