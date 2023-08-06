############################################################
# -*- coding: utf-8 -*-
#
# MOUNTCONTROL
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
############################################################
# standard libraries
import unittest
# external packages
# local imports
from mountcontrol.qtmount import Mount


class TestConfigData(unittest.TestCase):

    def setUp(self):
        pass

    #
    #
    # testing host
    #
    #

    def test_mac_ok1(self):
        mount = Mount()

        value = mount.checkFormatMAC('00:00:00:00:00:00')
        self.assertEqual('00:00:00:00:00:00', value)

    def test_mac_ok2(self):
        mount = Mount()

        value = mount.checkFormatMAC('00:aa:00:00:00:00')
        self.assertEqual('00:AA:00:00:00:00', value)

    def test_mac_ok3(self):
        mount = Mount()

        value = mount.checkFormatMAC('00:00:eF:00:00:00')
        self.assertEqual('00:00:EF:00:00:00', value)

    def test_mac_ok4(self):
        mount = Mount()

        value = mount.checkFormatMAC('00.00.00.00.00.00')
        self.assertEqual('00:00:00:00:00:00', value)

    def test_mac_ok4(self):
        mount = Mount()

        value = mount.checkFormatMAC('00.00.00:00:00.00')
        self.assertEqual('00:00:00:00:00:00', value)

    def test_mac_not_ok1(self):
        mount = Mount()

        value = mount.checkFormatMAC('00:00:000:00:00:00')
        self.assertEqual(None, value)

    def test_mac_not_ok2(self):
        mount = Mount()

        value = mount.checkFormatMAC('00:00:0:00:00:00')
        self.assertEqual(None, value)

    def test_mac_not_ok3(self):
        mount = Mount()

        value = mount.checkFormatMAC('00:00:00:00:00')
        self.assertEqual(None, value)

    def test_mac_not_ok4(self):
        mount = Mount()

        value = mount.checkFormatMAC('0h:00:00:00:00:00')
        self.assertEqual(None, value)
