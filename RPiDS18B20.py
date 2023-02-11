# SPDX-FileCopyrightText: 2019 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import glob
import time


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob( base_dir + '28*' )[1]
device_file = device_folder + '/w1_slave'
device_list = glob.glob( base_dir + '28*' )
print( f"Discovered devices: {device_list}" )


def read_lines_from_file():
  lines_list = []
  for device in device_list:
    print( f"Opening {device}" )
    with open( device + '/w1_slave', 'r' ) as device2:
      lines_list.append( device2.readlines() )
  print( f"lines_list: {lines_list}" )
  with open( device_file, 'r' ) as device:
    return device.readlines()


def read_temp():
  lines = read_lines_from_file()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep( 0.2 )
    lines = read_lines_from_file()
  equals_pos = lines[1].find( 't=' )
  if equals_pos != -1:
    temp_string = lines[1][equals_pos + 2:]
    temp_c = float( temp_string ) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c, temp_f


last_sensor_poll = 0
sensor_interval = 5  # Seconds

try:
  while True:
    if (time.time() - last_sensor_poll) > sensor_interval:
      print( read_temp() )
      last_sensor_poll = time.time()
except KeyboardInterrupt as interrupt:
  print( "Exiting..." )
