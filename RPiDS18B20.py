# SPDX-FileCopyrightText: 2019 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import glob
import time


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob( base_dir + '28*' )[1]
device_file = device_folder + '/w1_slave'


def read_lines_from_file():
  print( f"Opening '{glob.glob( base_dir + '28*' )}'" )
  with open( device_file, 'r' ) as device:
    return device.readlines()


def read_temp():
  lines = read_lines_from_file()
  print( f"lines: {lines}" )

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
