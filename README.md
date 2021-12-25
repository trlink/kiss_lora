# kiss_lora
LoRa / Kiss scripts to use a LoRa Modem with the ax25 tools / packet radio


This python script creates a virtual serial port (/dev/lora0) which can be used with the ax25 librarys to use packet radio over LoRa-Modems which are connected over SPI.

# Usage

You need to start the script as root (or with root rights (sudo)), otherwise the script can't create the lora device under /dev.

First you need to create an entry in /etc/ax25/axports:

lora    <Call Sign>          9600    200     2       Packet over LoRa
  
Configure the python script (Frequency and LoRa settings)
  
Start the script:
  
sudo python3 main.py

Open another terminal and use kissattach to attach the modem:
  
sudo kissattach /dev/lora0 lora

Now you can start linpac:
  
sudo linpac



