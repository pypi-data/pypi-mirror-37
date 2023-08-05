# pylint: disable=W1202,C0103
import sys
import threading
from murano_client.client import StoppableThread
from exoedge import logger

LOG = logger.getLogger(__name__)
# LOG.setLevel(logging.DEBUG)

class ExoEdgeSource(StoppableThread):
    """ Template class for defining custom "async" and/or "poll" type
    ExoEdge sources. Instances of this class will be a separate threads
    that follow the "borg" design pattern. """
    __borg_state = {}
    def __init__(self, **kwargs):
        """

        """
        self.__dict__ = self.__borg_state

        t_kwargs = {}
        if kwargs.get('group'):
            t_kwargs.update(group=kwargs.get('group'))
        if kwargs.get('target'):
            t_kwargs.update(target=kwargs.get('target'))
        if kwargs.get('name'):
            t_kwargs.update(name=kwargs.get('name'))
        if kwargs.get('args'):
            t_kwargs.update(args=kwargs.get('args'))
        if kwargs.get('kwargs'):
            t_kwargs.update(kwargs=kwargs.get('kwargs'))

        LOG.info("async source thread kwargs: {}".format(t_kwargs))
        LOG.info("async source other kwargs: {}".format(kwargs))

        super(ExoEdgeSource, self).__init__(**t_kwargs)
        self.setDaemon(True)

        self.config_io_thread = None
        for thread in threading.enumerate():
            if thread.getName() == "ConfigIO":
                self.config_io_thread = thread

    def get_channels_by_application(self, application):
        """
            Function for iterating over all channels and
            compiiing a list of channels that are configured
            for config_io.$(id).protocol_config.application
            equal to the 'application' parameter.
        """
        channels_by_application = []
        for c in self.config_io_thread.channels.values():
            if c.protocol_config.application == application:
                if c not in channels_by_application:
                    channels_by_application.append(c)
        return channels_by_application

    def get_source(self):
        """ Call this function atleast once to start the
        ExoEdgeSource thread. Call this function and assign
        to a variable to gain access to members and methods
        associated with this thread. """

        if not self.is_started():
            super(ExoEdgeSource, self).start()
        return self

# backwards compatibility with older versions of exoedge
AsyncSource = ExoEdgeSource
