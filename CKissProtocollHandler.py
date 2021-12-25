import time
import logging


FEND = 0xC0
FESC = 0xDB
TFEND= 0xDC
TFESC= 0xDD
            
KISSCMD_DATA = 0x0
KISSCMD_P = 0x02
KISSCMD_SlotTime = 0x03
KISSCMD_NoCmd = 0x80

KISSSTATE_VOID = 0x0
KISSSTATE_GETCMD = 0x1
KISSSTATE_GETDATA = 0x2
KISSSTATE_GETP = 0x3
KISSSTATE_GETSLOTTIME = 0x4
KISSSTATE_ESC = 0x5
  
class CKissProtocollHandler:
    
    def __init__(self, nMaxDataLen):
        
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        
        self.m_nMaxDataLen = nMaxDataLen
        self.m_logging = logging.getLogger("CKissProtocollHandler")
        self.m_logging.debug("Init CKissProtocollHandler, Buff size: " + str(nMaxDataLen))
        self.m_nKissState = KISSSTATE_VOID
        self.m_nKissCmd = KISSCMD_NoCmd
        self.m_bData = bytearray(b'')
        self.m_aPackets = []
        

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
            
            #bRes.append(FEND)
            #bRes.append(KISSCMD_DATA)
            
            for b in bData:
                
                #if b == FEND:
                #    bRes.append(FESC)
                #    bRes.append(TFEND)
                
                #elif b == FESC:
                #    bRes.append(FESC)
                #    bRes.append(TFESC)
                
                #else:
                bRes.append(b)
                                    
            #bRes.append(FEND)

        self.m_logging.debug("CKissProtocollHandler::Encode Result: " + str(len(bRes)) + " bytes of Data")

        return bRes
        
        