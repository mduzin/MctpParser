# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 20:06:18 2017

@author: M
"""

#MCTP PCIe VDM frame parser

import MctpParser

#Constatans
PCIE_VDM_HEADER_LEN = 16

def GetMctpPcieVdmRoutingType(RoutingType):
    Mctp_Routing_Type = {
        0b000 : 'Route to Root Complex',
        0b010 : 'Route by ID',
        0b011 : 'Broadcast from Root Complex'
        }
    return '{Type:#05b} : {Desc}'.format(Type = RoutingType, Desc = Mctp_Routing_Type.get(RoutingType,'Not supported for MCTP'))

def ParseMctpPcieVdmHeader(Header):
    Template = ""
    DataToDisplay = {}
    
    
    Result = Template.format(Data = DataToDisplay)
    print(Result)
    return Result


def ParseMctpPcieFrame(PcieFrame):
    #check basic frame size
    if len(PcieFrame) > PCIE_VDM_HEADER_LEN:
        #<TODO:>parse PCIe VDM Header
        #<TODO:>parse PCIe VDM Data (parse MCTP Frame)
        
        #Length of the PCIe VDM Data in bytes
        Length = PcieFrame[3] * 4
        PadLen = (PcieFrame[6] & 0x30)>>4
        MctpPacketPayload = PcieFrame[16:-PadLen]
        
        #check PCIe VDM Data Lenght. PCIe VDM Data starts from 16th byte
        if len(PcieFrame[16:]) == Length:
            #add MCTP Transport header bytes [12:16]
            MctpFrame = PcieFrame[12:16] + MctpPacketPayload
            MctpParser.ParseMctpFrame(MctpFrame)
        else:
            print("Error: Invalid MCTP PCIe VDM Data length.")
            print("PCIe VDM Header declares {0} bytes, but frame has only {1} bytes.\n\r".format(Length,len(PcieFrame[16:])))
   
    else:
        print("Error: Invalid MCTP PCIe VDM Frame length")
    return

#----Script Start----
if __name__ == "__main__":

    PcieTstFrame = [0x70, 0x00, 0x10, 0x01, 0x17, 0x00, 0x10, 0x7F, 0x00, 0x00, 0x1A, 0xB4, 0x01, 0x00, 0x00, 0xFB, 0x00, 0x82, 0x0D, 0x00]
    ParseMctpPcieFrame(PcieTstFrame)
    #RoutingTst = 0b000
    #print(GetMctpPcieVdmRoutingType(RoutingTst))
    
    #RoutingTst = 0b010
    #print(GetMctpPcieVdmRoutingType(RoutingTst))
    
    #RoutingTst = 0b011
    #print(GetMctpPcieVdmRoutingType(RoutingTst))
    
    #RoutingTst = 0b111
    #print(GetMctpPcieVdmRoutingType(RoutingTst))