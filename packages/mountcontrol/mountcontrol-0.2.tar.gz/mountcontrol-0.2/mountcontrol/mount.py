############################################################
# -*- coding: utf-8 -*-
#
# MOUNTCONTROL
#
# Python-based Tool for interaction with the 10micron mounts
#
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
############################################################
# standard libraries
import sys
import logging
import socket
# external packages
import wakeonlan
# local imports
from mountcontrol.firmware import Firmware
from mountcontrol.setting import Setting
from mountcontrol.obsSite import ObsSite
from mountcontrol.model import Model


__all__ = ['Mount',
           ]


class Mount(object):
    """
    The Mount class is the main interface for interacting with the mount computer.
    The user could:
        setup / change the interface to the mount
        start / stop cyclic tasks to poll data from mount
        send and get data from mount
        has signals for interfacing to external GUI's for data updates

        >>> settings = Mount(
        >>>                     host=host,
        >>>                     MAC=MAC,
        >>>                     pathToTS=pathToTS,
        >>>                     expire=expire,
        >>>                     verbose=verbose,
        >>>                 )

    """

    __all__ = ['Mount',
               ]
    version = '0.1'
    logger = logging.getLogger(__name__)

    # set timeout
    SOCKET_TIMEOUT = 0.5

    # 10 microns have 3492 as default port
    DEFAULT_PORT = 3492

    def __init__(self,
                 host=None,
                 MAC=None,
                 pathToTS=None,
                 expire=None,
                 verbose=None,
                 ):

        self._host = self.checkFormatHost(host)
        self._MAC = self.checkFormatMAC(MAC)
        self.pathToTS = pathToTS
        self.expire = expire
        self.verbose = verbose
        # signal handling
        self.mountUp = False

        # instantiating the data classes
        self.fw = Firmware(self.host)
        self.sett = Setting(self.host)
        self.model = Model(self.host)
        self.obsSite = ObsSite(self.host,
                               pathToTS=self.pathToTS,
                               expire=self.expire,
                               verbose=self.verbose,
                               )

    def checkFormatHost(self, value):
        """
        checkFormatHost ensures that the host ip and port is in correct format to enable
        socket connection later on. if no port is given, the default port for the mount
        will be added automatically

        :param      value: host value
        :return:    host value as tuple including port
        """

        if not value:
            self.logger.error('wrong host value: {0}'.format(value))
            return None
        if not isinstance(value, (tuple, str)):
            self.logger.error('wrong host value: {0}'.format(value))
            return None
        # now we got the right format
        if isinstance(value, str):
            value = (value, self.DEFAULT_PORT)
        return value

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        value = self.checkFormatHost(value)
        self._host = value
        # now setting to subclasses
        self.fw.host = value
        self.sett.host = value
        self.model.host = value
        self.obsSite.host = value

    @property
    def MAC(self):
        return self._MAC

    def checkFormatMAC(self, value):
        """
        checkFormatMAC makes some checks to ensure that the format of the string is ok for
        WOL package.

        :param      value: string with mac address
        :return:    checked string in upper cases
        """

        if not value:
            self.logger.error('wrong MAC value: {0}'.format(value))
            return None
        if not isinstance(value, str):
            self.logger.error('wrong MAC value: {0}'.format(value))
            return None
        value = value.upper()
        value = value.replace('.', ':')
        value = value.split(':')
        if len(value) != 6:
            self.logger.error('wrong MAC value: {0}'.format(value))
            return None
        for chunk in value:
            if len(chunk) != 2:
                self.logger.error('wrong MAC value: {0}'.format(value))
                return None
            for char in chunk:
                if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                'A', 'B', 'C', 'D', 'E', 'F']:
                    self.logger.error('wrong MAC value: {0}'.format(value))
                    return None
        # now we build the right format
        value = '{0:2s}:{1:2s}:{2:2s}:{3:2s}:{4:2s}:{5:2s}'.format(*value)
        return value

    @MAC.setter
    def MAC(self, value):
        value = self.checkFormatMAC(value)
        self._MAC = value

    def resetData(self):
        """
        resetData deletes all data already stored in classes just by redefining the
        classes. it send as well a signal, when the data is cleared.

        :return: nothing
        """

        self.fw = Firmware(self.host)
        self.sett = Setting(self.host)
        self.model = Model(self.host)
        self.obsSite = ObsSite(self.host,
                               pathToTS=self.pathToTS,
                               expire=self.expire,
                               verbose=self.verbose,
                               )

    def bootMount(self):
        """
        bootMount tries to boot the mount via WOL with a given MAC address

        :return:    True if success
        """

        if self.MAC is not None:
            wakeonlan.send_magic_packet(self.MAC)
            return True
        else:
            return False
