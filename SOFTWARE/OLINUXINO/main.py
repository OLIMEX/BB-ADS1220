#!/usr/bin/python python
# -*- coding: utf-8 -*-

# Demo program using Olimex BB-ADS1220 board
# Copyright (C) 2015 Stefan Mavrodiev, OLIMEX Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
__author__ = "Stefan Mavrodiev"
__copyright__ = "Copyright 2015, Olimex LTD"
__credits__ = ["Stefan Mavrodiev"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = __author__
__email__ = "support@olimex.com"

import argparse
import time
import sys

from ADS1220 import ADS1220
from pyA20.gpio import gpio
from pyA20.gpio import port


def wait_data():
    while gpio.input(irq):
        pass

# We will use PH0 port for IRQ
irq = port.PH0

gpio.init()
gpio.setcfg(irq, gpio.INPUT)

# ADS1120 is connected to UEXT1
ads = ADS1220("/dev/spidev2.0")

# Reset device
ads.command_reset()

time.sleep(0.1)

# First we will read temperature
ads.set_temperature_sensor_mode(1)
ads.command_start()

# Wait for IRQ gpio to be pulled low
wait_data()

# Read data
data = ads.read_data()

# Convert temperature
temperature = data[0] << 6 | data[1] >> 2

if not temperature & 0x2000:
    temperature *= 0.03125
else:
    temperature -= 1
    temperature = (~temperature & 0x3FFF)
    temperature *= -0.03125

sys.stdout.write("Temperature: %.5f C\n" % temperature)

# Monitor power supply
ads.command_reset()
time.sleep(0.1)
ads.set_mux(0x0d)
ads.set_conversion_mode(1)
ads.command_start()

while True:
    try:
        wait_data()
        readings = ads.read_data()
        vcc = readings[0] << 16 | readings[1] << 8 | readings[2]
        sys.stdout.write("\rAVDD: %.6fV" % (4*vcc*(2.048/pow(2, 23))))
        sys.stdout.flush()
    except KeyboardInterrupt:
        print("")
        break




