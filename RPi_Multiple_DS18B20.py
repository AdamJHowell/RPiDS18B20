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
import time

from DS18B20_Functions import device_list_populate, read_temp


if __name__ == "__main__":
  program_name = "RPi multiple DS18B20"
  loop_count = 0
  bus_scan_interval = 3600  # Rescan the 1-Wire bus every hour.
  sensor_interval = 10
  last_sensor_poll = 0

  # The 28* at the end of this directory will restrict the program to detect only DS18B20 devices.
  base_directory = "/sys/bus/w1/devices/28*"
  # This suffix is a subdirectory under the device, where the actual reading is located.
  device_folder_suffix = "/w1_slave"

  print( f"Welcome to {program_name}" )
  print( f"Sensors will be polled every {sensor_interval} seconds." )
  print( f"The 1-Wire bus will be scanned for new devices every {bus_scan_interval / 60} minutes." )
  # Create a List of every 1-wire device.
  device_list = device_list_populate( base_directory, device_folder_suffix )
  last_bus_scan = time.time()

  try:
    while True:
      if (time.time() - last_bus_scan) > bus_scan_interval:
        # Create a List of every 1-wire device.
        device_list = device_list_populate( base_directory, device_folder_suffix )
        last_bus_scan = time.time()
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
