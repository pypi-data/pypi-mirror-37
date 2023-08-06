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

def parse_addr(addr_str):
    """parse an IPv4 address, e.g. \"1.2.3.4:567\",
       return tuple of IP and port, e.g. ("1.2.3.4", 567), None on error"""
    fields = addr_str.split(":")
    if len(fields) > 2:
        return None
    ip = fields[0]
    port = fields[1]
    if len(ip.split(".")) != 4:
        return None
    try:
        port = int(port)
    except:
        return None
    if port < 0 or port > 65535:
        return None
    return (ip, port)

def parse_no(txt):
    """parse a decimal unsigned integer from string,
       e.g. \"12\", number, e.g. 12, None on error"""
    fields = txt.strip().split()
    if len(fields) > 1:
        return None
    try:
        no = int(fields[0])
    except:
        return None
    if no < 0:
        return None
    return no

def parse_two_nos(txt):
    """parse two comma separated decimal unsigned integers from string,
       e.g. \"12,34\", return tuple of two numbers, e.g. (12, 34),
       None on error"""
    fields = txt.strip().split()
    if len(fields) > 1:
        return None
    fields = fields[0].split(",")
    if len(fields) != 2:
        return None
    try:
        no1 = int(fields[0])
        no2 = int(fields[1])
    except:
        return None
    if no1 < 0 or no2 < 0:
        return None
    return (no1, no2)

