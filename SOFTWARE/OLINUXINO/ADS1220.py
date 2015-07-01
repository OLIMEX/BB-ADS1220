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

from pyA20 import spi


class ADS1220:

    # Configuration Register 0
    __mux = None
    __gain = None
    __pga_bypass = None

    # Configuration Register 1
    __dr = None     # Data rate
    __mode = None   # Operating mode
    __cm = None     # Conversion mode
    __ts = None     # Temperature sensor mode
    __bcs = None    # Burn-out current sources

    # Configuration Register 2
    __vref = None   # Voltage reference selection
    __fir = None    # FIR filter configuration
    __psw = None    # Low-side power switch configuration
    __idac = None   # IDAC current setting

    # Configuration Register 3
    __i1mux = None  # IDAC1 routing configuration
    __i2mux = None  # IDAC2 routing configuration
    __drdym = None  # DRDY mode

    def __init__(self, device):
        self.__spi = device

        spi.open(self.__spi, mode=1)

        # Reset the device and make sure that all registers are clear
        self.command_reset()

        #Check if all registers are zero
        for i in range(4):
            if self.read_register(i) != 0:
                raise IOError("Register is not cleared!")

        self.__update_register()

    def __exit__(self, exc_type, exc_val, exc_tb):
        spi.close()

    @staticmethod
    def read_register(register):
        return spi.xfer([0x20 | (register & 0x03) << 2], 1)[0]

    @staticmethod
    def write_register(register, data):
        spi.write([0x40 | (register & 0x03) << 2, data])

    @staticmethod
    def read_data():
        return spi.xfer([0x10], 3)

    def __update_register(self):
        # Read configuration register 0
        data = self.read_register(0)
        self.__pga_bypass = data & 0x01
        self.__gain = (data >> 1) & 0x07
        self.__mux = (data >> 4) & 0x0f

        # Read configuration register 1
        data = self.read_register(1)
        self.__bcs = data & 0x01
        self.__ts = (data >> 1) & 0x01
        self.__cm = (data >> 2) & 0x01
        self.__mode = (data >> 3) & 0x03
        self.__dr = (data >> 5) & 0x07

        # Read configuration register 2
        data = self.read_register(2)
        self.__idac = data & 0x07
        self.__psw = (data >> 3) & 0x01
        self.__fir = (data >> 4) & 0x03
        self.__vref = (data >> 6) & 0x03

        # Read configuration register 3
        data = self.read_register(3)
        self.__drdym = (data >> 1) & 0x01
        self.__i2mux = (data >> 2) & 0x07
        self.__i1mux = (data >> 5) & 0x07

    # Commands
    @staticmethod
    def command_reset():
        """
        RESET (0000 011x)

        Resets the device to the default values. Wait at least (50us + 32 · t(CLK)) after the RESET command is sent
        before sending any other command.
        """
        spi.write([0x06])

    def command_start(self):
        """
        START/SYNC (0000 100x)

        In single-shot mode, the START/SYNC command is used to start a single conversion, or (when sent during an
        ongoing conversion) to reset the digital filter, and then restarts a single new conversion. When the device is
        set to continuous conversion mode, the START/SYNC command must be issued one time to start converting
        continuously. Sending the START/SYNC command while converting in continuous conversion mode resets the
        digital filter and restarts continuous conversions.
        """

        # Make sure that PGA is disabled if AINn = AVSS
        if 0x07 < self.__mux < 0x0c:
            if not self.__pga_bypass:
                raise ValueError("When AINn = AVSS internal low-noise PGA must be disabled!")
            if self.__gain > 0x02:
                raise ValueError("When AINn = AVSS only gain 1, 2 and 4 can be used")
        spi.write([0x08])

    @staticmethod
    def command_power_down():
        """
        POWERDOWN (0000 001x)

        The POWERDOWN command places the device into power-down mode. This command shuts down all internal analog
        components, opens the low-side switch, turns off both IDACs, but holds all register values. In case the
        POWERDOWN command is issued while a conversion is ongoing, the conversion completes before the ADS1220 enters
        power-down mode. As soon as a START/SYNC command is issued, all analog components return to their previous
        states.
        """
        spi.write([0x02])

    # Registers
    def set_mux(self, mux):
        """
        Input multiplexer configuration

        These bits configure the input multiplexer.
        For settings where AINN = AVSS, the PGA must be disabled (PGA_BYPASS = 1) and
        only gains 1, 2, and 4 can be used.

        :param mux: See datasheet for more information
        """

        # Check value
        if not 0 <= mux <= 0xe:
            raise ValueError("Invalid value for mux")

        # Write register
        self.write_register(0, ((self.read_register(0) & ~0xf0) | (mux & 0x0f) << 4))

        # Read back value
        self.__update_register()

        if self.__mux != mux:
            raise IOError("Failed to set input multiplexer configuration")

    def set_gain(self, gain):
        """
        Gain configuration

        These bits configure the device gain. Gains 1, 2, and 5 can be used without the PGA,
        In this case, gain is obtained by a switched-capacitor structure.

        :param gain: Gain = 2^gain
        """

        # Check value
        if not 0 <= gain <= 7:
            raise ValueError("Invalid value for gain")

         # Write register
        self.write_register(0, ((self.read_register(0) & ~0x0e) | (gain & 0x07) << 1))

        # Read back value
        self.__update_register()

        if self.__gain != gain:
            raise IOError("Failed to set gain configuration")

    def set_pga_bypass(self, pga_bypass):
        """
        Disables and bypasses the internal low-noise PGA

        Disabling the PGA reduces overall power consumption and allows the common-mode voltage range (Vcm) to
        span from AVSS-0.1V to AVDD+0.1V.
        The PGA can only be disabled for gains 1, 2, and 4.
        The PGA is always enabled for gain settings 8 to 128, regardless of the PGA_BYPASS setting.

        :param pga_bypass:  0: PGA enabled
                            1: PGA disabled and bypassed
        """
        # Check value
        if not 0 <= pga_bypass <= 1:
            raise ValueError("Invalid value for pga_bypass")

        # Write register
        self.write_register(0, ((self.read_register(0) & ~0x01) | (pga_bypass & 0x01)))

        # Read back value
        self.__update_register()

        if self.__pga_bypass != pga_bypass:
            raise IOError("Failed to set PGA bypass")

    def set_data_rate(self, data_rate):
        """
        Data rate

        These bits control the data rate setting depending on the selected operating mode.
        :param data_rate: See table 18 in the datasheet
        """

        # Check value
        if not 0 <= data_rate <= 7:
            raise ValueError("Invalid value for data_rate")

        # Write register
        self.write_register(1, ((self.read_register(1) & ~0xe0) | (data_rate << 5)))

        # Read back value
        self.__update_register()

        if self.__dr != data_rate:
            raise IOError("Failed to set data rate")

    def set_mode(self, mode):
        """
        Operating mode

        These bits control the operating mode the device operates in.

        :param mode:    0 - normal mode
                        1 - Duty-cycle mode
                        2 - Turbo mode
        """

        # Check value
        if not 0 <= mode <= 2:
            raise ValueError("Invalid value for mode")

        # Write register
        self.write_register(1, ((self.read_register(1) & ~0x18) | (mode << 3)))

        # Read back value
        self.__update_register()

        if self.__mode != mode:
            raise IOError("Failed to set mode")

    def set_conversion_mode(self, cm):
        """
        Conversion mode

        This bit sets the conversion mode for the device.

        :param cm:    0 - Single-shot mode
                        1 - Continuous conversion mode
        """

        # Check value
        if not 0 <= cm <= 1:
            raise ValueError("Invalid value for cm")

        # Write register
        self.write_register(1, ((self.read_register(1) & ~0x04) | (cm << 2)))

        # Read back value
        self.__update_register()

        if self.__cm != cm:
            raise IOError("Failed to set conversion mode")

    def set_temperature_sensor_mode(self, ts):
        """
        Temperature sensor mode

        This bit enables the internal temperature sensor and puts the device in temperature sensor mode.
        The settings of configuration register 0 have no effect and the device uses the internal
        reference for measurement when temperature sensor mode is enabled.

        :param ts:  0 - Disables temperature sensor
                    1 - Enables temperature sensor
        """

        # Check value
        if not 0 <= ts <= 1:
            raise ValueError("Invalid value for ts")

        # Write register
        self.write_register(1, ((self.read_register(1) & ~0x02) | (ts << 1)))

        # Read back value
        self.__update_register()

        if self.__ts != ts:
            raise IOError("Failed to set temperature sensor mode")

    def set_burn_out(self, bcs):
        """
        Burn-out current sources

        This bit controls the 10- A, burn-out current sources.
        The burn-out current sources ca be used to detect sensor faults such as wire breaks and
        shorted sensors.

        :param bcs:  0 - Current sources off
                    1 - Current sources on
        """

        # Check value
        if not 0 <= bcs <= 1:
            raise ValueError("Invalid value for bcs")

        # Write register
        self.write_register(1, ((self.read_register(1) & ~0x01) | bcs))

        # Read back value
        self.__update_register()

        if self.__bcs != bcs:
            raise IOError("Failed to set burn-out current sources")

    def set_vref(self, vref):
        """
        Voltage reference selection

        These bits select the voltage reference source that is used for the conversion.

        :param vref:    0 : Internal 2.048V reference selected
                        1 : External reference selected using dedicated REFP0 and REFN0 inputs
                        2 : External reference selected using AIN0/REFP1 and AIN3/REFN1 inputs
                        3 : Analog supply (AVDD - AVSS) used as reference
        """

        # Check value
        if not 0 <= vref <= 3:
            raise ValueError("Invalid value for vref")

        # Write register
        self.write_register(2, ((self.read_register(2) & ~0xc0) | (vref << 6)))

        # Read back value
        self.__update_register()

        if self.__vref != vref:
            raise IOError("Failed to set vref")

    def set_fir(self, fir):
        """
        FIR filter configuration

        These bits configure the filter coefficients for the internal FIR filter.
        These bits only affect the 20-SPS setting in normal mode and 5-SPS setting in duty-cycle mode

        :param fir: 0 : No 50-Hz or 60-Hz rejection
                    1 : Simultaneous 50-Hz and 60-Hz rejection
                    2 : 50-Hz rejection only
                    3 : 60-Hz rejection only
        """

        # Check value
        if not 0 <= fir <= 3:
            raise ValueError("Invalid value for fir")

        # Write register
        self.write_register(2, ((self.read_register(2) & ~0x30) | (fir << 4)))

        # Read back value
        self.__update_register()

        if self.__fir != fir:
            raise IOError("Failed to set FIR")

    def set_psw(self, psw):
        """
        Low-side power switch configuration

        These bit configures the behavior of the low-side switch connected between AIN3/REFN1 and AVSS

        :param psw: 0 : Switch is always open
                    1 : Switch automatically closes when the START/SYNC command is sent and opens
                    when the POWERDOWN command is issued
        """

        # Check value
        if not 0 <= psw <= 1:
            raise ValueError("Invalid value for psw")

        # Write register
        self.write_register(2, ((self.read_register(2) & ~0x08) | (psw << 3)))

        # Read back value
        self.__update_register()

        if self.__psw != psw:
            raise IOError("Failed to set power switch configuration")

    def set_idac(self, idac):
        """
        IDAC current setting

        These bits set the current for both IDAC1 and IDAC2 excitation current sources.

        :param idac:    0 : Off
                        1 : 10uA
                        2 : 50uA
                        3 : 100uA
                        4 : 250uA
                        5 : 500uuA
                        6 : 1000uA
                        7 : 1500uA
        """

        # Check value
        if not 0 <= idac <= 7:
            raise ValueError("Invalid value for idac")

        # Write register
        self.write_register(2, ((self.read_register(2) & ~0x07) | idac))

        # Read back value
        self.__update_register()

        if self.__idac != idac:
            raise IOError("Failed to set IDAC")

    def set_i1mux(self, i1mux):
        """
        IDAC1 routing configuration

        These bits select the channel where IDAC1 is routed to

        :param i1mux:   0 : IDAC1 disabled
                        1 : IDAC1 connected to AIN0/REFP1
                        2 : IDAC1 connected to AIN1
                        3 : IDAC1 connected to AIN2
                        4 : IDAC1 connected to AIN3/REFN1
                        5 : IDAC1 connected ot REFP0
                        6 : IDAC1 connected to REFN0
        """

        # Check value
        if not 0 <= i1mux <= 6:
            raise ValueError("Invalid value for i1mux")

        # Write register
        self.write_register(3, ((self.read_register(3) & ~0xe0) | (i1mux << 5)))

        # Read back value
        self.__update_register()

        if self.__i1mux != i1mux:
            raise IOError("Failed to set IDAC1")

    def set_i2mux(self, i2mux):
        """
        IDAC2 routing configuration

        These bits select the channel where IDAC2 is routed to

        :param i1mux:   0 : IDAC2 disabled
                        1 : IDAC2 connected to AIN0/REFP1
                        2 : IDAC2 connected to AIN1
                        3 : IDAC2 connected to AIN2
                        4 : IDAC2 connected to AIN3/REFN1
                        5 : IDAC2 connected ot REFP0
                        6 : IDAC2 connected to REFN0
        """

        # Check value
        if not 0 <= i2mux <= 6:
            raise ValueError("Invalid value for i2mux")

        # Write register
        self.write_register(3, ((self.read_register(3) & ~0x1c) | (i2mux << 2)))

        # Read back value
        self.__update_register()

        if self.__i2mux != i2mux:
            raise IOError("Failed to set IDAC2")

    def set_drdym(self, drdym):
        """
        DRDY mode

        This bit controls the behavior of the DOUT/DRDY pin when new data are ready.

        :param drdym:   0 : Only the dedicated DRDY pin is used to indicate when data are ready
                        1 : Data ready is indicated simultaneously on DOUT/DRDY and DRDY
        """

        # Check value
        if not 0 <= drdym <= 1:
            raise ValueError("Invalid value for drdym")

        # Write register
        self.write_register(3, ((self.read_register(3) & ~0x02) | (drdym << 1)))

        # Read back value
        self.__update_register()

        if self.__drdym != drdym:
            raise IOError("Failed to set DRDY mode")