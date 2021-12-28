# kiss_lora
LoRa / Kiss scripts to use a LoRa Modem with the ax25 tools / packet radio


This python script creates a virtual serial port (/dev/lora0) which can be used with the ax25 librarys to use packet radio over LoRa-Modems which are connected via SPI.

# Usage

You need to start the script as root (or with root rights (sudo)), otherwise the script can't create the lora device under /dev.

  
# config
  
Copy the cfg-file to /etc and change the settings to match your system (Hardware connection, Frequency and LoRa settings)
  
Start the script:
  
sudo python3 main.py

If the script starts and creates the lora0 device, create an ax25 port:

You need to create an entry in /etc/ax25/axports:

lora    <Call Sign>          9600    200     2       Packet over LoRa

Keep in mind, that the LoRa Modems can't send packets > 255 bytes, I limited it to 250 and discarded the initial plan to use the KISS protocoll (the data is already sent in packets) 

# start 
  
Open another terminal and use kissattach to attach the modem:
  
sudo kissattach /dev/lora0 lora

  
Now you can start linpac:
  
sudo linpac

  
# service
  
To start the script a service, you can copy the .service file to the systemd services and start it over systemd...

  
# compile 

This script uses a modified version of PyLora (https://github.com/Inteform/PyLora), I attached it in the PyLora.7z File, check instructions on the original page to build and install the library...


  


