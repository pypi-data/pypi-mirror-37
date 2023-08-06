# python EtherPix library
#
# Copyright 2017 Stefan Schuermans <stefan schuermans info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from struct import Struct


class Mapping(object):

    RED = 0
    WHITE = 0 # red and white share first mapping
    GREEN = 1
    BLUE = 2
    CHANNELS = 3

    def __init__(self):
        """create a new color mapping for an EtherPix distributor"""
        self._base = 0.0
        self._gamma = 1.0
        self._factor = 1.0
        self._precompute()

    def set_params(self, base, factor, gamma):
        """set mapping parameters"""
        self._base = base
        self._gamma = gamma
        self._factor = factor
        self._precompute()

    def _precompute(self):
        """pre-compute mapping table"""
        # display_value := base + factor * input_value ^ (1 / gamma)
        gamma_1 = 1.0 / self._gamma
        s = Struct("!B")
        tab = []
        for v in range(256):
            display_val = self._base + self._factor * (v / 255.0) ** gamma_1
            if display_val < 0:
                display_no = 0
            elif display_val > 1.0:
                display_no = 255
            else:
                display_no = int(round(display_val * 255.0))
            tab.append(s.pack(display_no))
        self.table = tuple(tab)

