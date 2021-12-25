import time
import logging
import os, pty, serial
from lora02_modem import CLoRa02_Modem
from CKissProtocollHandler import CKissProtocollHandler
from SerialEmulator import SerialEmulator


#https://github.com/sh123/lora_arduino_kiss_modem/blob/master/lora_arduino_kiss_modem.ino
#sudo python3 -m serial.tools.miniterm /dev/lora0

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        
g_log = logging.getLogger("main")
g_nMaxProtoLen = 128
g_modem = None


def initHardware():
    #variables
    ##########
    global g_modem
    
    #modem = CLoRa02_Modem("/dev/spidev0.0", 24, 22, 16)
    g_modem = CLoRa02_Modem("/dev/spidev0.0", 24, 22, 16)
    g_modem.SetModemOptions({"Frequency": 433000000, "SF": 10, "BW": 125000, "Preamble": 200, "SW": 99, "CR": 4})
    
    if g_modem.InitModem() == True:
        return True
    else:
        g_log.error("Failed to initialize LoRa-Module")
        
        #init with wrong CS, on next call, it could work...
        g_modem = CLoRa02_Modem("/dev/spidev0.0", 25, 22, 16)
        g_modem.InitModem()
        
        time.sleep(2)
        
        return initHardware()
        

if __name__ == "__main__":
    #variables
    ##########
    #global g_modem
    kissSerial = CKissProtocollHandler(g_nMaxProtoLen)


    g_log.info("Start LoRa02 to KISS Bridge")
    
    if initHardware() == True:
        emulator = SerialEmulator('./ttydevice','/dev/lora0', 9600) 
    
        g_log.debug("Created virtual ports")

        bHavePacket = False
        
        while True:
            
            bData = b'' 
            bData = emulator.read()
            
            if len(bData) > 0:
                
                g_log.debug("Serial: received: " + str(len(bData)))
                
                if kissSerial.addData(bData) == True:
                    
                    bHavePacket = True
                    
            if bHavePacket == True:
                
                if g_modem.isReceiving() == False:
                    bHavePacket = False
                    bData = kissSerial.getPacket()
            
                    if len(bData) > 0:
                        g_log.debug("LoRa: Transmit Data: " + str(len(bData)))
                        g_modem.SendData(bData)
                        
                    else:
                        g_log.error("Could not transmit Data - empty packet: " + str(len(bData)))
                        
                        
                else:
                    g_log.debug("Could not Transmit Data - Modem RX state, wait!")
                    
                        
                
            bData = g_modem.ReceiveData()
            
            if len(bData) > 0:
                
                g_log.debug("LoRa: Received " + str(len(bData)) + " bytes over LoRa")
                
                bData = kissSerial.encodePacket(bData)
                
                g_log.debug("Serial: write: " + str(len(bData)))
                
                emulator.write(bData)
                
            time.sleep(0.2)
        
    else:
        g_log.eror("Unable to init hardware")
                