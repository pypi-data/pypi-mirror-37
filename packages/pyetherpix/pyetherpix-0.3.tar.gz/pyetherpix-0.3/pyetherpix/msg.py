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

from __future__ import print_function
import sys


class Msg(object):

    ERR = 1
    WARN = 2
    INFO = 3

    def __init__(self):
        """interface for message callback object"""

    def msg(self, level, text):
        """message is delivered
           level: ERR for errors, WARN for warnings, INFO for information
           text: message text"""
        raise NotImplementedError("Msg.msg is not implemented")


class MsgDef(Msg):

    def __init__(self, level=Msg.INFO):
        """default message callback implementation
           level: level of messages to output"""
        Msg.__init__(self)
        self._level = level

    def msg(self, level, text):
        """message is delivered
           level: ERR for errors, WARN for warnings, INFO for information
           text: message text"""
        if level == Msg.ERR:
          prefix = "error"
        elif level == Msg.WARN:
          prefix = "warning"
        elif level == Msg.INFO:
          prefix = "info"
        else:
          prefix = "unknown"
        if level <= self._level:
          print(prefix + ": " + text, file=sys.stderr)

