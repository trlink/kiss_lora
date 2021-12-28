import time
import logging
import zlib


  
class CKissProtocollHandler:
    
    def __init__(self, nMaxDataLen):
        
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        
        self.m_nMaxDataLen = nMaxDataLen
        self.m_logging = logging.getLogger("CKissProtocollHandler")
        self.m_logging.debug("Init CKissProtocollHandler, Buff size: " + str(nMaxDataLen))
        self.m_bData = bytearray(b'')
        self.m_aPackets = []
        
        
    def haveData(self):
        if len(self.m_aPackets) > 0:
            return True
        else:
            return False
        

    def addData(self, bData):
        bPacketComplete = True
        
        self.m_aPackets.append(bData)
        
        self.m_logging.debug("CKissProtocollHandler: added serial packet to queue at: " + str(len(self.m_aPackets) - 1) + " size: " + str(len(bData)))

        return bPacketComplete
    
    
    def getPacket(self):
        bRes = bytearray(b'')
        
        if len(self.m_aPackets) > 0:
            bRes = self.m_aPackets[0]
            self.m_aPackets.pop(0)
            
            self.m_logging.debug("CKissProtocollHandler: returned serial packet from queue, remaining: " + str(len(self.m_aPackets)) + " size: " + str(len(bRes)))
        
        return bRes


    def encodePacket(self, bData):
        bRes =  bytearray(b'')
        
        self.m_logging.debug("CKissProtocollHandler::Encode: " + str(len(bData)) + " bytes of Data")
        
        if len(bData) > 0:
            bRes = bData

        self.m_logging.debug("CKissProtocollHandler::Encode Result: " + str(len(bRes)) + " bytes of Data")

        return bRes
        
        