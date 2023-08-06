##
#     Project: PyKerio
# Description: API for Kerio products
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import os
import ssl
import unittest

import pykerio


class TestCase_Storage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Prepares session
        """
        # Ignore invalid certificates
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        # API object
        api = pykerio.PyKerioControl(
            server=os.environ.get('KERIO_SERVER', 'control-demo.kerio.com'),
            port=int(os.environ.get('KERIO_PORT', '4081')))
        # ApiApplication object
        application = pykerio.structs.ApiApplication({
            'name': cls.__name__,
            'vendor': pykerio.constants.APP_NAME,
            'version': pykerio.constants.APP_VERSION})

        # Session login
        cls.session = pykerio.interfaces.Session(api)
        cls.session.login(userName=os.environ.get('KERIO_USERNAME', 'admin-en'),
                          password=os.environ.get('KERIO_PASSWORD', 'kerio'),
                          application=application)

        # Storage
        cls.storage = pykerio.interfaces.Storage(api)

    @classmethod
    def tearDownClass(cls):
        """
        Closes session
        """
        cls.session.logout()

    def test_01_get(self):
        """
        Test Storage get
        """
        storage_list = self.__class__.storage.get()
        self.assertNotEquals(len(storage_list), 0)
        for storage in storage_list:
            self.assertEquals(type(storage), pykerio.structs.StorageData)

    @unittest.skipIf(os.environ.get('KERIO_READONLY', 'NO').upper() == 'YES',
                     'Insufficient rights')
    def test_02_remove(self):
        """
        Test Storage remove
        """
        self.__class__.storage.remove(pykerio.enums.StorageDataType(
            name='StorageDataLogs'))
