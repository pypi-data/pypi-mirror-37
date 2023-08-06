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

import unittest

import pykerio


class TestCase_Error(unittest.TestCase):
    def test_01_Error(self):
        """
        Test Error
        """
        positional_parameters = pykerio.lists.StringList()
        positional_parameters.append('User1')
        positional_parameters.append('Foo')

        message = 'Would you want to delete the user %1 (%2)?'
        messageparameters = pykerio.structs.LocalizableMessageParameters({
            'positionalParameters': positional_parameters,
            'plurality': 1})
        index = 2
        code = 32614
        teststruct = pykerio.structs.Error({
            'inputIndex': index,
            'code': code,
            'message': message,
            'messageParameters': messageparameters})
        self.assertEquals(len(teststruct.keys()), 4)
        self.assertEquals(len(teststruct.values()), 4)

        self.assertEquals(teststruct['inputIndex'], index)
        self.assertEquals(teststruct['code'], code)
        self.assertEquals(teststruct['message'], message)
        self.assertEquals(teststruct['messageParameters'],
                          messageparameters)

        teststruct.clear()
        self.assertEquals(len(teststruct.keys()), 0)
