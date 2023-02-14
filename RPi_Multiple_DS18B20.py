"""
Source: https://www.hackster.io/vinayyn/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi-d8a6b0
"""
import glob
import time


def device_list_populate():
  print( f"Discovered devices:" )
  list_of_devices = []
  for index, discovered_device in enumerate( glob.glob( base_dir ) ):
    print( f"  {index} - {discovered_device}" )
    list_of_devices.append( discovered_device + device_folder_suffix )
  return list_of_devices


# Read the temperature from each folder
def read_from_sensor( file ):
  with open( file, 'r' ) as device_file:
    lines = device_file.readlines()
    # print( f"read_temp_raw() lines: {lines}" )
    return lines


# Convert the temperature data to a human-readable format.
def read_temp( device_to_read ):
  lines = read_from_sensor( device_to_read )
  while lines[0].strip()[-3:] != 'YES':
    lines = read_from_sensor( device_to_read )
  equals_pos = lines[1].find( 't=' )
  temp_string = lines[1][equals_pos + 2:]
  temp_c = float( temp_string ) / 1000.0
  temp_f = temp_c * 9.0 / 5.0 + 32.0
  return temp_c, temp_f


if __name__ == "__main__":
  program_name = "RPi multiple DS18B20"
  base_dir = "/sys/bus/w1/devices/28*"
  device_folder_suffix = "/w1_slave"

  print( f"Welcome to {program_name}" )
  device_list = device_list_populate()
  print( f"Detected {len( device_list )} devices." )
  try:
    while True:
      # Iterate through the device_list, reading and printing each temperature.
      for count, device in enumerate( device_list, start = 1 ):
        print( f"  Sensor {count}: %3.3f°C  %3.3f°F" % read_temp( device ) )
      time.sleep( 5 )
  except KeyboardInterrupt:
    print()
    print( "Keyboard interrupt detected." )
  finally:
    print( f"Goodbye from {program_name}" )
