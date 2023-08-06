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

from ..pykerio import PyKerio

from ..enums import StorageDataType

from ..lists import StorageDataList


class Storage(object):
    def __init__(self, api: PyKerio):
        self.api = api

    def get(self):
        """
        Returns list of data present on storage.
        """
        response = self.api.request_rpc(
            method='Storage.get',
            params={})
        results = StorageDataList()
        results.load(response.result['data'])
        return results

    def remove(self, storage_type: StorageDataType):
        """
        Delete data specified by type from storage.
        """
        response = self.api.request_rpc(
            method='Storage.remove',
            params={'type': storage_type.dump()})
