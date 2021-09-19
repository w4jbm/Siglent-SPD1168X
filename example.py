# Siglent SPD1168X Status and Control API
#
# Based on version for the dual supply version
# by Saulius Lukse, Copyright 2015-2018
#
# This adaptation is by Jim McClanahan, W4JBM
# Copyright 2021
#
# Licensed under GNU GPLv3

import siglent_psu_api as siglent
import time

s = siglent.SIGLENT_PSU("192.168.10.231")

# read instrument identification string
print("Fetching system identification...")
i = s.identify()
print(i)

# read instrument status
print("\nFetching system status...")
sys = s.system()
print(sys)


# set CH1 voltage to 5V
s.set(siglent.CHANNEL.CH1, siglent.PARAMETER.VOLTAGE, 5.0)
time.sleep(1)

# switch on CH1
s.output(siglent.CHANNEL.CH1, siglent.STATE.ON)
time.sleep(1)

# read voltage
rv = s.measure(ch = siglent.CHANNEL.CH1, parameter = siglent.PARAMETER.VOLTAGE)
rc = s.measure(ch = siglent.CHANNEL.CH1, parameter = siglent.PARAMETER.CURRENT)

print(f'\nVoltage: {rv}, Current: {rc}')
