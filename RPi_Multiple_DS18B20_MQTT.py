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

import paho.mqtt.client as mqtt

import MQTT_Functions
from DS18B20_Functions import device_list_populate, read_temp, check_bus, set_bus


if __name__ == "__main__":
  program_name = "RPi multiple DS18B20"
  loop_count = 0
  bus_scan_interval = 3600  # Rescan the 1-Wire bus every hour.
  power_gpio = 17
  sensor_interval = 10
  last_sensor_poll = 0
  broker_address = "192.168.55.200"
  broker_port = 1883
  topic = "Office/piz2-2/DS18B20"
  mqtt_client = mqtt.Client( client_id = "MQTTS Client ID" )
  mqtt_client.on_connect = MQTT_Functions.connect_callback_v3
  mqtt_client.on_disconnect = MQTT_Functions.disconnect_callback_v3
  mqtt_client.on_subscribe = MQTT_Functions.subscribe_callback_v3
  mqtt_client.on_message = MQTT_Functions.on_message_callback_v3
  mqtt_client.on_unsubscribe = MQTT_Functions.unsubscribe_callback_v3
  mqtt_client.loop_start()
  if mqtt_client.connect( broker_address, port = broker_port ):
    print( f"Successfully connected to {broker_address}:{broker_port}" )
  else:
    print( f"Failed to connect to {broker_address}:{broker_port}" )

  # The 28* at the end of this directory will restrict the program to detect only DS18B20 devices.
  base_directory = "/sys/bus/w1/devices/28*"
  # This suffix is a subdirectory under the device, where the actual reading is located.
  device_folder_suffix = "/w1_slave"
  set_bus( power_gpio )

  print( f"Welcome to {program_name}" )
  print( f"The 1-Wire bus will be scanned for new devices every {bus_scan_interval / 60} minutes." )
  print( f"Temperature sensors on the bus will be polled every {sensor_interval} seconds." )
  # Create a List of every 1-wire device.
  device_list = device_list_populate( base_directory, device_folder_suffix )
  last_bus_scan = time.time()

  try:
    if (time.time() - last_bus_scan) > bus_scan_interval:
      # Create a List of every 1-wire device.
      device_list = device_list_populate( base_directory, device_folder_suffix )
      last_bus_scan = time.time()
    while True:
      if (time.time() - last_sensor_poll) > sensor_interval:
        check_bus()
        loop_count += 1
        # Iterate through the device_list, reading and printing each temperature.
        for count, device in enumerate( device_list, start = 1 ):
          temp_c = read_temp( device )
          print( f"  Sensor {count}: {temp_c:.2f}°C  {(temp_c * 1.8 + 32):.2f}°F" )
          mqtt_client.publish( f"{topic}-{count}/tempF", f"{(temp_c * 1.8 + 32):.2f}" )
        print()
        last_sensor_poll = time.time()
  except KeyboardInterrupt:
    print( "\n" )
    print( "Keyboard interrupt detected." )
  finally:
    print( f"Goodbye from {program_name}" )
