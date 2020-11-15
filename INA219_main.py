

# Copyright (c) 2019 Robert Nelson <robert.nelson@digikey.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from ina219 import INA219
from machine import I2C,Pin
import sys
import time

print("#Booting Up...")

# Instantiate an I2C peripheral.
i2c=I2C(scl=Pin(4), sda=Pin(5))
for address in i2c.scan():
    print("- I2C device found at address: %s" % hex(address))



print("#Online...")

TARGET_64BIT_ADDR = b'\x00\x13\xA2\x00\x41\xA7\xAD\xBC'

#ina219:
#A0:A1
# 1:1 = 0x45 Solar
# 0:1 = 0x44 Battery
# 1:0 = 0x41 5VoltRail
# 0:0 = 0x40 12VoltRail

SOLAR_INA219A_ADDR = 0x40

SHUNT_OHMS = 0.1

def read_solar():
    try:
        solar_voltage = str(solar_ina.voltage())
        solar_current = str(solar_ina.current())
        print_solar = "Solar:" + time_snapshot + ":BusVolt:" + solar_voltage + "V:Current:" + solar_current + "mA:#"
    except:
        print_solar = "Solar:" + time_snapshot + ":BusVolt:INVALID:Current:INVALID:#"
        print("INA219:0x45: Solar read failed...")

    try:
        print(TARGET_64BIT_ADDR, print_solar)
    except:
        print("XBee: TX Solar Failed...")

solar_ina = INA219(SHUNT_OHMS, i2c, SOLAR_INA219A_ADDR)
try:
    print("INA219:0x45: Configuring solar...")
    solar_ina.configure_32v_2a()
except:
    print("INA219:0x45: Solar Missing...")

while True:
    time_snapshot = str(time.ticks_cpu())
    read_solar()
    time.sleep(1)


