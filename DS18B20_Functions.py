import glob
import os
import time

import RPi.GPIO as GPIO


def device_list_populate( base_dir, directory_suffix = "" ):
  """
  This function will detect devices under the base directory, and append the directory suffix to each one before returning them all in one List
  I have only tested this with DS18B20 sensors, but it should work for other devices like the DS2413.
  :param base_dir: The filesystem directory where the devices are located
  :type base_dir: String
  :param directory_suffix: An optional suffix to append to each discovered device
  :type directory_suffix: String
  :return: A List of directories
  :rtype: List of Strings
  """
  check_bus()
  print( "Discovered devices:" )
  list_of_devices = []
  # Use glob to detect all devices on the filesystem.
  for index, discovered_device in enumerate( glob.glob( base_dir ), start = 1 ):
    print( f"  {index} - {discovered_device}" )
    # Add each device to the List.
    list_of_devices.append( discovered_device + directory_suffix )
  print()
  return list_of_devices


# Read the temperature from each folder
def read_from_sensor( device_file ):
  """
  This function will read all available lines from a device on the filesystem
  :param device_file: The path to a device
  :type device_file: String
  :return: A list of every line returned by the device
  :rtype: List of Strings
  """
  with open( device_file, 'r' ) as device_file:
    lines = device_file.readlines()
    # print( f"read_temp_raw() lines: {lines}" )
    return lines


# Convert the temperature data to a human-readable format.
def read_temp( device_to_read ):
  """
  This will parse the DS18B20-specific output, to find the temperature in Celsius
  :param device_to_read: The location on the filesystem of the device to read from
  :type device_to_read: String
  :return: The temperature in Celsius
  :rtype: String
  """
  lines = read_from_sensor( device_to_read )
  while lines[0].strip()[-3:] != "YES":
    lines = read_from_sensor( device_to_read )
  equals_pos = lines[1].find( "t=" )
  temp_string = lines[1][equals_pos + 2:]
  return float( temp_string ) / 1000.0


def check_bus():
  power_gpio = 17
  power_off_time = 3
  power_on_time = 5
  if not os.path.isdir( "/sys/bus/w1/devices/28-xxxxxxxxxx" ):
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( power_gpio, GPIO.OUT )
    GPIO.output( power_gpio, GPIO.LOW )
    time.sleep( power_off_time )
    GPIO.output( power_gpio, GPIO.HIGH )
    time.sleep( power_on_time )
