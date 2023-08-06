#! /usr/bin/env python

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

import sys
import time

from PIL import Image

import pyetherpix


def main(argv):
    if len(argv) < 2:
        print >>sys.stderr, "usage: %s <config.etp>" % argv[0]
        return 2
    config_file = argv[1]
    # create display
    display = pyetherpix.Display(config_file)
    (width, height) = display.get_size()
    print("width %u, height %u" % (width, height))
    # prepare "on" image (all white)
    on = Image.new("RGB", (width, height), "white")
    # blink
    print("blink")
    for i in range(5):
        print("on")
        display.data_image(on)
        display.send()
        time.sleep(0.5)
        print("off")
        display.data_clear()
        display.send()
        time.sleep(0.5)
    print("done")
    # close display
    display.close()
    return 0


if __name__ == "__main__":
  sys.exit(main(sys.argv))

