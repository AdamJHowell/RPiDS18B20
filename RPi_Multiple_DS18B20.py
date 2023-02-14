"""
This program will read from any number of DS18B20 temperature sensors connected to a Raspberry Pi.
What my program does differently than others, is the dynamic detection and configuration of all connected devices.

The Raspberry Pi must have the Dallas 1-wire protocol enabled on the Interfaces tab of the Raspberry Pi Configuration utility.
Once that interface is enabled and the Pi rebooted, the 1-wire devices will appear on the Raspberry Pi filesystem.

This is a modification of another program that hard-coded each sensor.
That project had a lot of repeated code, and had to be updated teach time a sensor was added or removed.
The original hard-coded project can be found here: https://www.hackster.io/vinayyn/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi-d8a6b0
I suspect that project was derived from the Adafruit project located here: https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Raspberry_Pi_DS18B20_Temperature_Sensing/code.py
"""
import glob
import time


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
  print( "Discovered devices:" )
  list_of_devices = []
  # Use glob to detect all devices on the filesystem.
  for index, discovered_device in enumerate( glob.glob( base_dir ) ):
    print( f"  {index} - {discovered_device}" )
    # Add each device to the List.
    list_of_devices.append( discovered_device + directory_suffix )
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


if __name__ == "__main__":
  program_name = "RPi multiple DS18B20"
  loop_count = 0
  sensor_interval = 10
  last_sensor_poll = 0

  # The 28* at the end of this directory will restrict the program to detect only DS18B20 devices.
  base_directory = "/sys/bus/w1/devices/28*"
  # This suffix is a subdirectory under the device, where the actual reading is located.
  device_folder_suffix = "/w1_slave"

  print( f"Welcome to {program_name}" )
  # Create a List of every 1-wire device.
  device_list = device_list_populate( base_directory, device_folder_suffix )
  print( f"Sensors will be polled every {sensor_interval} seconds." )

  try:
    while True:
      if (time.time() - last_sensor_poll) > sensor_interval:
        loop_count += 1
        # Iterate through the device_list, reading and printing each temperature.
        for count, device in enumerate( device_list, start = 1 ):
          temp_c = read_temp( device )
          print( f"  Sensor {count}: {temp_c:.2f}°C  {(temp_c * 1.8 + 32):.2f}°F" )
        print()
        last_sensor_poll = time.time()
  except KeyboardInterrupt:
    print( "\n" )
    print( "Keyboard interrupt detected." )
  finally:
    print( f"Goodbye from {program_name}" )
