import PyLora
import time
import logging
from modem import CModem




class CLoRa02_Modem(CModem):
    
    def __init__(self, strDevice, nCs_Pin, nRst_Pin, nIrq_Pin):
        self.m_bError = False
        self.m_lFreq = 433000000
        self.m_nSpreadFactor = 10
        self.m_nBandwidth = 125000
        self.m_nPreamble = 200
        self.m_nSyncWord = 99
        self.m_nCodingRate = 4
        self.m_strDevice = strDevice
        self.m_nCs_Pin = nCs_Pin
        self.m_nRst_Pin = nRst_Pin
        self.m_nIrqPin = nIrq_Pin
        
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        
        self.m_logging = logging.getLogger("CLoRa02_Modem")
        self.m_logging.debug('Create LoRa02 Instance at ' + self.m_strDevice)
        
        
    def SetModemOptions(self, dOptions):
        
        for key in dOptions:
            
            self.m_logging.debug('Set Option ' + key + ": " + str(dOptions[key]))
            
            if key == "SF":
                self.m_nSpreadFactor = dOptions[key]
                
            if key == "Frequency":
                self.m_lFreq = dOptions[key]
            
            if key == "BW":
                self.m_nBandwidth = dOptions[key]
                
            if key == "Preamble":
                self.m_nPreamble = dOptions[key]
                
            if key == "SW":
                self.m_nSyncWord = dOptions[key]
                
            if key == "CR":
                self.m_nCodingRate = dOptions[key]
    
    
    def isReceiving(self):
        return PyLora.isReceiving()
    
                
    def InitModem(self):
        
        self.m_bError = False
        self.m_logging.info('Init LoRa02 Instance')
        self.m_logging.debug('Device: ' + self.m_strDevice)
        self.m_logging.debug('CS_PIN: ' + str(self.m_nCs_Pin))
        self.m_logging.debug('RST_PIN: ' + str(self.m_nRst_Pin))
        self.m_logging.debug('IRQ_PIN: ' + str(self.m_nIrqPin))
        
        
        PyLora.set_pins(spi_device=self.m_strDevice, cs_pin=self.m_nCs_Pin, rst_pin=self.m_nRst_Pin, irq_pin=self.m_nIrqPin)

        if PyLora.init() == 1:
            PyLora.reset()
            PyLora.set_frequency(self.m_lFreq)
            PyLora.set_spreading_factor(self.m_nSpreadFactor)
            PyLora.set_bandwidth(self.m_nBandwidth)
            PyLora.set_preamble_length(self.m_nPreamble)
            PyLora.set_sync_word(self.m_nSyncWord)
            PyLora.set_coding_rate(self.m_nCodingRate)
            PyLora.enable_crc()
            
            time.sleep(2)
            
            if PyLora.get_frequency() != self.m_lFreq:
                
                self.m_logging.error("Init failed Freq mismatch: " + str(PyLora.get_frequency()))
            
                PyLora.close()
                
                self.m_bError = True
                
                return False
            else:
                
                self.m_logging.debug('Init success!')
            
                return True
        else:
            self.m_logging.error("Init comm failed!")
            
            self.m_bError = True
            
            return False
        
        
        
    def ReceiveData(self):
        
        if self.m_bError == False:
            PyLora.receive()
                
            if PyLora.packet_available() == True:
        
                return PyLora.receive_packet()
                
        return b''
        
        
        
    def SendData(self, bData):
        if self.m_bError == False:
            PyLora.send_packet(bData)
            return True
        else:
            return False
  





if __name__ == "__main__":
    modem = CLoRa02_Modem("/dev/spidev0.0", 24, 22, 16)
    modem.SetModemOptions({"Frequency": 433000000, "SF": 10, "BW": 125000, "Preamble": 200, "SW": 99, "CR": 4})
    modem.InitModem()
    
    
  

#PyLora.explicit_header_mode()

#while True:
#    PyLora.send_packet(bytes("Hello\0", encoding="utf-8"))
#    print ('Packet sent...')
#    time.sleep(2)

#PyLora.lora_dump_register()



