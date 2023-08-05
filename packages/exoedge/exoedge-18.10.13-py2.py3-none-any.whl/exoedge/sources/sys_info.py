"""
    An ExoEdge source that provided convenient access to system information and resources.
"""
# pylint: disable=W1202,C0111
import logging
import time
import threading
import platform as _platform
import sys as _sys
import getpass as _getpass
import json
import threading
import psutil as _psutil
from exoedge.sources import ExoEdgeSource
from exoedge import logger

logger.getLogger(__name__)


def architecture():
    """
        Get the system architecture.
    """
    tmp = _platform.architecture()
    if isinstance(tmp, tuple):
        depth = tmp[0]
    else:
        depth = tmp
    return depth

def machine_type():
    """
        Get the machine type.
    """
    return _platform.machine()

def platform():
    """
        Get the machine platform info.
    """
    return _platform.platform()

def python_version():
    """
        Get the version of Python currently in use.
    """
    return 'Python {}'.format(_platform.python_version())

def whoami():
    """
        Get the current user.
    """
    return _getpass.getuser()

def net_io():
    """
        Get usage statistics on all system net interfaces.
    """
    payload = {}
    ioc = _psutil.net_io_counters(pernic=True)
    for iface in ioc:
        if not payload.get(iface):
            payload[iface] = {}
        for elem in dir(ioc[iface]):
            if not elem.startswith('_'):
                if ioc[iface].__dict__.get(elem):
                    payload[iface][elem] = ioc[iface].__dict__[elem]
    return payload

def disk_stats():
    """
        Get current usage on all mountpoints.
    """
    payload = {}
    mountpoints = [p.mountpoint for p in _psutil.disk_partitions()]
    for mp in mountpoints:
        usage = _psutil.disk_usage(mp)
        if not payload.get(mp):
            payload[mp] = {}
        for elem in dir(usage):
            if not elem.startswith('_'):
                if usage.__dict__.get(elem):
                    payload[mp][elem] = usage.__dict__[elem]
    return payload

def cpu_times_percent(interval=1):
    cpus = _psutil.cpu_times_percent(interval=interval, percpu=True)
    payload = {}
    cpunum = 0
    for cpu in cpus:
        cpunum += 1
        if not payload.get(cpu):
            payload[cpunum] = {}
        for elem in dir(cpu):
            if not elem.startswith('_'):
                if cpu.__dict__.get(elem):
                    payload[cpunum][elem] = cpu.__dict__[elem]
    return payload


def machine_info():
    """
        Get human readable info on the target machine.
    """
    return '\n'.join([
        platform(),
        machine_type(),
        bit_depth(),
        python_version(),
        whoami(),
    ])

