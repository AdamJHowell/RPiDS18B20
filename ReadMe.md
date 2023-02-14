# Raspberry Pi DS18B20

### A simple program to read the temperature from one or more DS18B20 sensors

This program will read from any number of DS18B20 temperature sensors connected to a Raspberry Pi. What my program does differently than others, is the dynamic detection and configuration of all connected devices.

This is a modification of another program that hard-coded each sensor. That project had a lot of repetitious code, and had to be modified each time a sensor was added or removed.

The original hard-coded project [can be found here](https://www.hackster.io/vinayyn/multiple-ds18b20-temp-sensors-interfacing-with-raspberry-pi-d8a6b0).

I suspect that project was derived from the Adafruit project [located here](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Raspberry_Pi_DS18B20_Temperature_Sensing/code.py).

#### Notes:
* The Raspberry Pi must have the Dallas 1-wire protocol enabled on the Interfaces tab of the Raspberry Pi Configuration utility.
* Once that interface is enabled and the Pi rebooted, the 1-wire devices will appear on the Raspberry Pi filesystem.
