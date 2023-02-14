"""
Source: https://www.hackster.io/vinayyn/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi-d8a6b0
"""
import glob
import os
import time


device_address_suffix = "28*"
device_folder_suffix = "/w1_slave"
device_folder_name = "/name"

# These lines mount the device:
os.system( 'modprobe w1-gpio' )
os.system( 'modprobe w1-therm' )

base_dir = '/sys/bus/w1/devices/'
# Get all the filenames that begin with 28 in the path base_dir.
device_folder = glob.glob( base_dir + '28*' )[0]
print( f"device_folder: {device_folder}" )
device_folder1 = glob.glob( base_dir + '28*' )[1]
print( f"device_folder1: {device_folder1}" )

device_file = device_folder + '/w1_slave'
print( f"device_file: {device_file}" )
device_file1 = device_folder1 + '/w1_slave'
print( f"device_file1: {device_file1}" )


def read_rom():
  name_file = device_folder + '/name'
  f = open( name_file, 'r' )
  # print('f:',f)
  return f.readline()


def read_rom1():
  name_file1 = device_folder1 + '/name'
  g = open( name_file1, 'r' )
  # print('g:',g)
  return g.readline()


# Read the temperature from each folder
def read_temp_raw():
  with open( device_file, 'r' ) as device:
    lines = device.readlines()
    # print( f"read_temp_raw() lines: {lines}" )
    return lines


def read_temp_raw1():
  with open( device_file1, 'r' ) as device1:
    lines1 = device1.readlines()
    # print( f"read_temp_raw()1 lines: {lines1}" )
    return lines1


# Convert the temperature data to a human-readable format.
def read_temp():
  temp_c = 0.0
  temp_f = 0.0
  lines = read_temp_raw()
  while lines[0].strip()[-3:] != 'YES':
    lines = read_temp_raw()
  equals_pos = lines[1].find( 't=' )
  temp_string = lines[1][equals_pos + 2:]
  temp_c = float( temp_string ) / 1000.0
  temp_f = temp_c * 9.0 / 5.0 + 32.0
  return temp_c, temp_f


def read_temp1():
  temp_c1 = 0.0
  temp_f1 = 0.0
  lines1 = read_temp_raw1()
  while lines1[0].strip()[-3:] != 'YES':
    lines1 = read_temp_raw1()
  equals_pos1 = lines1[1].find( 't=' )
  temp_string1 = lines1[1][equals_pos1 + 2:]
  temp_c1 = float( temp_string1 ) / 1000.0
  temp_f1 = temp_c1 * 9.0 / 5.0 + 32.0
  return temp_c1, temp_f1


while True:
  # Read the temperature data and print the value from each individual sensor.
  print( ' C1=%3.3f  F1=%3.3f' % read_temp() )
  print( ' C2=%3.3f  F2=%3.3f' % read_temp1() )
  time.sleep( 5 )
