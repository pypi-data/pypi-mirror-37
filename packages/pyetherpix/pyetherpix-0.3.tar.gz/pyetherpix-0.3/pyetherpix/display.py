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

import socket

from pyetherpix.distributor import Distributor
from pyetherpix.mapping import Mapping
from pyetherpix.msg import Msg, MsgDef
from pyetherpix.parse import parse_addr, parse_no, parse_two_nos


class Display(object):

    def __init__(self, config_file, msg_obj=None):
        """create a new EtherPix display
           config_file: name of config file to read
           msg_obj: message callback object or None"""
        self._msg = msg_obj
        if self._msg is None: # use default message callback if none given
            self._msg = MsgDef()
        # default settings
        self._bind_addr = ("0.0.0.0", 0) # local network address to bind to
        self._size = (0, 0) # size of display
        self._distris = {}
        # read config file
        if not self._proc_config_file(config_file):
            raise Exception("error(s) while reading config file")
        # create and bind socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setblocking(False)
        self._socket.bind(self._bind_addr)

    def close(self):
        """close display"""
        self._socket.close()

    def get_size(self):
        """get size of display as (width, height) in pixels"""
        return self._size

    def data_clear(self):
        """clear image data, i.e. set entire image to black"""
        for distri in self._distris.values():
          distri.data_clear()

    def data_image(self, image):
        """set image data
           image: Pillow RGB Image object"""
        for distri in self._distris.values():
          distri.data_image(image)

    def send(self):
        """send image data to actual distributor modules using UDP"""
        for distri in self._distris.values():
          distri.send(self._socket)

    def _proc_config_distri(self, setting, value, lineno):
        """process distributor line from config file"""
        # distributor number
        distri_str = setting.split(" ", 1)[1]
        distri_no = parse_no(distri_str)
        if distri_no is None:
            self._msg.msg(Msg.ERR, "invalid distributor number \"%s\""
                                   " in line %u of config file" %
                                   (distri_str, lineno))
            return False
        # number of outputs and pixels per output
        outputs_pixels = parse_two_nos(value)
        if outputs_pixels is None:
             self._msg.msg(Msg.ERR, "invalid distributor size \"%s\""
                                    " in line %u of config file" %
                                    (value, lineno))
             return False
        (outputs, pixels) = outputs_pixels
        # check if distributor is already present
        if distri_no in self._distris:
             self._msg.msg(Msg.ERR, "duplicate defintion of distributor %u"
                                    " in line %u of config file" %
                                    (distri_no, lineno))
             return False
        # create distributor
        self._distris[distri_no] = Distributor(distri_no, outputs, pixels)
        return True

    def _proc_config_file(self, config_file):
        """process config file
           config_file: name of config file to read
           returns True on success, False on error"""
        self._msg.msg(Msg.INFO, "using config file \"%s\"" % config_file)
        # process all lines in config file
        okay = True
        try:
            with open(config_file, "r") as cfile:
                lineno = 1
                for line in cfile:
                   if not self._proc_config_line(line, lineno):
                       okay = False
                   lineno += 1
        except (IOError, OSError) as e:
            self._msg.msg(Msg.ERR, str(e))
            okay = False
        # set default address of all distributors without address
        for distri in self._distris.values():
            distri.def_addr()
        return okay

    def _proc_config_distri_addr(self, setting, value, lineno):
        """process distributor address line from config file"""
        # distributor number
        distri_str = setting.split(" ", 1)[1]
        distri_no = parse_no(distri_str)
        if distri_no is None:
            self._msg.msg(Msg.ERR, "invalid distributor number \"%s\""
                                   " in line %u of config file" %
                                   (distri_str, lineno))
            return False
        # number of outputs and pixels per output
        addr = parse_addr(value)
        if addr is None:
             self._msg.msg(Msg.ERR, "invalid distributor address \"%s\""
                                    " in line %u of config file" %
                                    (value, lineno))
             return False
        # check if distributor exists
        if distri_no not in self._distris:
             self._msg.msg(Msg.ERR, "no distributor with number %u"
                                    " in line %u of config file" %
                                    (distri_no, lineno))
             return False
        # add address to distributor
        self._distris[distri_no].add_addr(addr)
        return True

    def _proc_config_line(self, line, lineno):
        """process line from config file
           line: line read from config file
           lineno: line number
           returns True on success, False on error"""
        # parse config file line "setting = value # comment"
        line_no_comment = line.split("#", 1)[0].strip()
        if line_no_comment == "":
            return True # ignore empty lines
        else:
            fields = line_no_comment.split("=", 1)
            if len(fields) < 2:
                self._msg.msg(Msg.WARN,
                              "invalid line %u in config file, ignored"
                              % lineno)
                return True
            else:
                setting = fields[0].strip()
                value = fields[1].strip()
                return self._proc_config_setting(setting, value, lineno)

    def _proc_config_mapping(self, setting, value, lineno):
        """process mapping line from config file"""
        fields = setting.split()
        if len(fields) != 3:
            self._msg.msg(Msg.ERR, "invalid mapping specifier \"%s\""
                                   " in line %u of config file" %
                                   (setting, lineno))
            return False
        # distributor number
        distri_str = fields[1]
        distri_no = parse_no(distri_str)
        if distri_no is None:
            self._msg.msg(Msg.ERR, "invalid distributor number \"%s\""
                                   " in line %u of config file" %
                                   (distri_str, lineno))
            return False
        # color channel
        color_str = fields[2]
        if color_str == "red":
            channels = 3
            color = Mapping.RED
        elif color_str == "green":
            channels = 3
            color = Mapping.GREEN
        elif color_str == "blue":
            channels = 3
            color = Mapping.BLUE
        elif color_str == "white":
            channels = 1
            color = Mapping.WHITE
        else:
            self._msg.msg(Msg.ERR, "invalid color channel \"%s\""
                                   " in line %u of config file" %
                                   (color_str, lineno))
            return False
        # mapping parameters
        params = value.split()
        if len(params) != 3:
            self._msg.msg(Msg.ERR, "invalid mapping parameters \"%s\""
                                   " in line %u of config file" %
                                   (value, lineno))
            return False
        try:
            base = float(params[0])
        except:
            self._msg.msg(Msg.ERR, "invalid base value \"%s\""
                                   " in line %u of config file" %
                                   (params[0], lineno))
            return False;
        try:
            factor = float(params[1])
        except:
            self._msg.msg(Msg.ERR, "invalid factor value \"%s\""
                                   " in line %u of config file" %
                                   (params[1], lineno))
            return False;
        try:
            gamma = float(params[2])
            if gamma <= 0.0:
                raise ValueError
        except:
            self._msg.msg(Msg.ERR, "invalid gamma value \"%s\""
                                   " in line %u of config file" %
                                   (params[2], lineno))
            return False
        # check if distributor exists
        if distri_no not in self._distris:
             self._msg.msg(Msg.ERR, "no distributor with number %u"
                                    " in line %u of config file" %
                                    (distri_no, lineno))
             return False
        # set mapping
        self._distris[distri_no].set_mapping(color, base, factor, gamma)
        # update number of channels
        self._distris[distri_no].set_channels(channels)
        return True

    def _proc_config_output(self, setting, value, lineno):
        """process output line from config file"""
        fields = setting.split()
        if len(fields) != 2:
            self._msg.msg(Msg.ERR, "invalid output specifier \"%s\""
                                   " in line %u of config file" %
                                   (setting, lineno))
            return False
        # distributor number and output number
        distri_output_str = fields[1]
        distri_output = parse_two_nos(distri_output_str)
        if distri_output is None:
            self._msg.msg(Msg.ERR, "invalid distributor/output numbers \"%s\""
                                   " in line %u of config file" %
                                   (distri_output_str, lineno))
            return False
        (distri_no, output_no) = distri_output
        # check if distributor exists
        if distri_no not in self._distris:
             self._msg.msg(Msg.ERR, "no distributor with number %u"
                                    " in line %u of config file" %
                                    (distri_no, lineno))
             return False
        # get distributor
        distri = self._distris[distri_no]
        # check if output exists
        if not distri.check_output_no(output_no):
             self._msg.msg(Msg.ERR, "no output with number %u for distributor"
                                    " %u in line %u of config file" %
                                    (output_no, distri_no, lineno))
             return False
        # split pixels and check number
        max_pixels = distri.get_pixels()
        pixel_data = value.split()
        if len(pixel_data) < max_pixels:
             self._msg.msg(Msg.ERR, "too many pixels (%u, more than %u)"
                                    " for distributor %u, output %u"
                                    " in line %u of config file" %
                                    (len(pixel_data), max_pixels,
                                     distri_no, output_no, lineno))
             return False
        # parse pixels
        err = False
        pixel_coords = []
        i = 0
        for pixel_str in pixel_data:
            pixel_xy = parse_two_nos(pixel_str)
            if pixel_xy is None:
                self._msg.msg(Msg.ERR, "invalid pixel coordinates \"%s\""
                                       " for pixel %u"
                                       " at distributor %u, output %u"
                                       " in line %u of config file" %
                                       (pixel_str, i,
                                        distri_no, output_no, lineno))
                err = True
            else:
                if pixel_xy[0] < 0 or pixel_xy[0] >= self._size[0] or \
                   pixel_xy[1] < 0 or pixel_xy[1] >= self._size[1]:
                    self._msg.msg(Msg.ERR, "pixel coordinates %u,%u"
                                           " outside of frame for pixel %u"
                                           " at distributor %u, output %u"
                                           " in line %u of config file" %
                                           (pixel_xy, i,
                                            distri_no, output_no, lineno))
                    pixel_xy = None
                    err = True
            pixel_coords.append(pixel_xy)
            i += 1
        if err:
            return False
        # set pixels
        distri.set_pixel_coords(output_no, pixel_coords)
        return True

    def _proc_config_setting(self, setting, value, lineno):
        """process setting from config file
           setting: name of setting
           value: value of setting
           returns True on success, False on error"""
        # replace all whitespace sequences in setting with single spaces
        setting = " ".join(setting.split())
        # process setting
        if setting == "bindAddr":
            addr = parse_addr(value)
            if addr is None:
                self._msg.msg(Msg.ERR,
                              "invalid address \"%s\" for \"bindAddr\""
                              " in line %u in config file"
                              % (value, lineno))
                return False
            else:
                self._bind_addr = addr
                self._msg.msg(Msg.INFO,
                              "bind address \"%s:%u\"" % (addr[0], addr[1]))
                return True
        elif setting == "size":
            size = parse_two_nos(value)
            if size is None:
                self._msg.msg(Msg.ERR,
                              "invalid address \"%s\" for \"size\""
                              " in line %u in config file"
                              % (value, lineno))
                return False
            else:
                self._size = size
                return True
        elif setting.startswith("distributor "):
            return self._proc_config_distri(setting, value, lineno)
        elif setting.startswith("distributorAddr "):
            return self._proc_config_distri_addr(setting, value, lineno)
        elif setting.startswith("mapping "):
            return self._proc_config_mapping(setting, value, lineno)
        elif setting.startswith("output "):
            return self._proc_config_output(setting, value, lineno)
        else:
            self._msg.msg(Msg.WARN,
                          "unknown setting \"%s\" in line %u in config file,"
                          " ignored" % (setting, lineno))
            return True

