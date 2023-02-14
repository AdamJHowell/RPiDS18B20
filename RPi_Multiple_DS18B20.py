"""
Source: https://www.hackster.io/vinayyn/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi-d8a6b0
"""
import glob
import time


program_name = "RPi multiple DS18B20"
base_dir = "/sys/bus/w1/devices/28*"
device_folder_suffix = "/w1_slave"

# Get all the filenames that begin with 28 in the path base_dir.
# device_file = glob.glob( base_dir )[0] + device_folder_suffix
# device_file1 = glob.glob( base_dir )[1] + device_folder_suffix


def device_list_populate():
  list_of_devices = []
  for index, item in enumerate( glob.glob( base_dir ) ):
    print( index, item )
    list_of_devices.append( item + device_folder_suffix )
  return list_of_devices


def device_count():
  list_of_devices = glob.glob( base_dir )
  for discovered_device in list_of_devices:
    print( f"  Device found at directory: {discovered_device}" )
  return len( list_of_devices )


# Read the temperature from each folder
def read_temp_raw( file ):
  with open( file, 'r' ) as device_file:
    lines = device_file.readlines()
    # print( f"read_temp_raw() lines: {lines}" )
    return lines


# Convert the temperature data to a human-readable format.
def read_temp( file_to_read ):
  lines = read_temp_raw( file_to_read )
  while lines[0].strip()[-3:] != 'YES':
    lines = read_temp_raw( file_to_read )
  equals_pos = lines[1].find( 't=' )
  temp_string = lines[1][equals_pos + 2:]
  temp_c = float( temp_string ) / 1000.0
  temp_f = temp_c * 9.0 / 5.0 + 32.0
  return temp_c, temp_f


if __name__ == "__main__":
  print( f"Welcome to {program_name}" )
  device_list = device_list_populate()
  print( f"Detected {device_count()} devices." )
  try:
    while True:
      # Read the temperature data and print the value from each individual sensor.
      for device in device_list:
        print( ' C1=%3.3f  F1=%3.3f' % read_temp( device ) )
      # print( ' C2=%3.3f  F2=%3.3f' % read_temp( device_file1 ) )
      time.sleep( 5 )
  except KeyboardInterrupt:
    print()
    print( "Keyboard interrupt detected." )
  finally:
    print( f"Goodbye from {program_name}" )
