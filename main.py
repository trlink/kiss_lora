import time
import logging
import os, pty, serial
import sys
from lora02_modem import CLoRa02_Modem
from CKissProtocollHandler import CKissProtocollHandler
from SerialEmulator import SerialEmulator
import configparser



#https://github.com/sh123/lora_arduino_kiss_modem/blob/master/lora_arduino_kiss_modem.ino
#sudo python3 -m serial.tools.miniterm /dev/lora0

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        

g_nErrCount = 0;
g_log = logging.getLogger("main")
g_nMaxProtoLen = 128
g_modem = None
g_strDev = ""
g_nRST = 0;
g_nIRQ = 0
g_nCS = 0
g_lFreq = 0
g_nSF = 0
g_nBandwidth = 0
g_bPreamble = 0
g_nSyncWord = 0
g_nCodingRate = 0


def initHardware():
    #variables
    ##########
    global g_modem
    global g_nErrCount
    global g_lFreq
    global g_nSF
    global g_nBandwidth
    global g_bPreamble
    global g_nSyncWord
    global g_nCodingRate
    global g_strDev
    global g_nRST
    global g_nIRQ
    global g_nCS

    
    #modem = CLoRa02_Modem("/dev/spidev0.0", 24, 22, 16)
    g_modem = CLoRa02_Modem(g_strDev, g_nCS, g_nRST, g_nIRQ)
    g_modem.SetModemOptions({"Frequency": g_lFreq, "SF": g_nSF, "BW": g_nBandwidth, "Preamble": g_bPreamble, "SW": g_nSyncWord, "CR": g_nCodingRate})
    
    if g_modem.InitModem() == True:
        return True
    else:
        g_log.error("Failed to initialize LoRa-Module")
        g_nErrCount += 1;
        
        if g_nErrCount > 5:
            g_log.error("Can't init modem, give up...")
            
            return False;
        
        #init with wrong CS, on next call, it could work...
        g_modem = CLoRa02_Modem(g_strDev, g_nCS + 1, g_nRST, g_nIRQ)
        g_modem.InitModem()
        
        time.sleep(2)
        
        return initHardware()
        

if __name__ == "__main__":
    #variables
    ##########
    #global g_modem
    kissSerial = CKissProtocollHandler(g_nMaxProtoLen)


    g_log.info("Start LoRa02 to Serial Bridge")
    
    config = configparser.ConfigParser()
    config.read('/etc/seriallora.cfg')

    try:
        g_strDev = config["modem"]["device"]
        g_nRST = int(config["modem"]["RST"])
        g_nIRQ = int(config["modem"]["IRQ"])
        g_nCS = int(config["modem"]["CS"])
        g_lFreq = int(config["lora"]["freq"])
        g_nSF = int(config["lora"]["SF"])
        g_nBandwidth = int(config["lora"]["BW"])
        g_bPreamble = int(config["lora"]["Preamble"])
        g_nSyncWord = int(config["lora"]["SyncWord"])
        g_nCodingRate = int(config["lora"]["CodingRate"])      

    except:
        g_log.error("could not read config, check config!")

        sys.exit(-1)

        
    if initHardware() == True:
        
        try:
            emulator = SerialEmulator('./ttydevice','/dev/lora0', 9600) 
        except:
            g_log.error("could not Create virtual ports - start with root rights!")

            sys.exit(-1)

        
        g_log.debug("Created virtual ports")

        bHavePacket = False
        
        while True:
            
            bData = b'' 
            bData = emulator.read()
            
            if (len(bData) > 0):
                
                if (len(bData) <= 250):
                
                    g_log.debug("Serial: received: " + str(len(bData)))
                    kissSerial.addData(bData)
                
                else:
                    
                    g_log.warning("Serial: packet over max trx size, received: " + str(len(bData)))
            
            
            bHavePacket = kissSerial.haveData()      
                    
            if bHavePacket == True:
                
                if g_modem.isReceiving() == False:
                    
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
        
        sys.exit(-1)