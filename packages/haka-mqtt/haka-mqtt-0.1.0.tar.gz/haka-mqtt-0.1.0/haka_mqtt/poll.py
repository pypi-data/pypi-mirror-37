import ssl
from select import select

from haka_mqtt.clock import SystemClock
from haka_mqtt.dns_async import AsyncFutureDnsResolver
from haka_mqtt.reactor import ReactorProperties, Reactor, INACTIVE_STATES
from haka_mqtt.scheduler import Scheduler
from haka_mqtt.socket_factory import SslSocketFactory, socket_factory


class _PollClientSelector(object):
    def __init__(self, async_dns_resolver):
        self.__rmap = {async_dns_resolver.read_fd(): async_dns_resolver.poll}
        self.__wmap = {}

    def add_read(self, fd, reactor):
        """
        Parameters
        ----------
        fd: file descriptor
            File-like object.
        reactor: haka_mqtt.reactor.Reactor
        """
        self.__rmap[fd] = reactor.read

    def del_read(self, fd, reactor):
        """
        Parameters
        ----------
        fd: file descriptor
            File-like object.
        reactor: haka_mqtt.reactor.Reactor
        """
        del self.__rmap[fd]

    def add_write(self, fd, reactor):
        """
        Parameters
        ----------
        fd: file descriptor
            File-like object.
        reactor: haka_mqtt.reactor.Reactor
        """
        self.__wmap[fd] = reactor.write

    def del_write(self, fd, reactor):
        """
        Parameters
        ----------
        fd: file descriptor
            File-like object.
        reactor: haka_mqtt.reactor.Reactor
        """
        del self.__wmap[fd]

    def select(self, select_timeout=None):
        rlist, wlist, xlist = select(self.__rmap.keys(), self.__wmap.keys(), [], select_timeout)
        for fd in rlist:
            self.__rmap[fd]()

        for fd in wlist:
            self.__wmap[fd]()


class MqttPollClientProperties(object):
    def __init__(self):
        self.host = None
        self.port = None
        self.client_id = None
        self.keepalive_period = None
        self.ssl = True
        self.ip6 = True
        self.ip4 = True


class MqttPollClient(Reactor):
    """

    Parameters
    ----------
    properties: MqttPollClientProperties
    """
    def __init__(self, properties, log='haka'):
        self.__clock = SystemClock()
        self.__scheduler = Scheduler()
        self.__async_name_resolver = AsyncFutureDnsResolver()
        self.__selector = _PollClientSelector(self.__async_name_resolver)

        endpoint = (properties.host, properties.port)

        p = ReactorProperties()
        if properties.ssl:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            p.socket_factory = SslSocketFactory(ssl_context, properties.host)
        else:
            p.socket_factory = socket_factory

        p.endpoint = endpoint
        p.keepalive_period = properties.keepalive_period
        p.client_id = properties.client_id
        p.scheduler = self.__scheduler
        p.name_resolver = self.__async_name_resolver
        p.selector = self.__selector

        self.__last_poll_time = None

        Reactor.__init__(self, p, log=log)

    def start(self):
        Reactor.start(self)
        self.__last_poll_time = None

    def poll(self, period=0.):
        if period is None:
            poll_end_time = None
        else:
            poll_end_time = self.__clock.time() + period

        if self.__last_poll_time is None:
            self.__last_poll_time = self.__clock.time()

        select_timeout = self.__scheduler.remaining()
        while (poll_end_time is None or self.__clock.time() < poll_end_time) and self.state not in INACTIVE_STATES:
            #
            #                                 |---------poll_period-------------|------|
            #                                 |--poll--|-----select_period------|
            #                                 |  dur   |
            #  ... ----|--------|-------------|--------|---------|--------------|------|---- ...
            #            select   handle i/o     poll     select    handle i/o    poll
            #
            self.__selector.select(select_timeout)

            poll_time = self.__clock.time()
            time_since_last_poll = poll_time - self.__last_poll_time

            self.__scheduler.poll(time_since_last_poll)
            self.__last_poll_time = poll_time

            select_timeout = self.__scheduler.remaining()
            if select_timeout is not None:
                last_poll_duration = self.__clock.time() - self.__last_poll_time
                select_timeout -= last_poll_duration

            if select_timeout is not None and select_timeout < 0:
                select_timeout = 0
