# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 20:06:18 2017
@author: M
"""

#MCTP PCIe VDM frame parser

import MctpParser

#Constatans
PCIE_VDM_HEADER_LEN = 16

def GetMctpPcieBdfAddress(Frame,FieldDesc = "PCI BDF Address"):
    Template = ""
    if len(Frame) == 2:
        Template += "{FirstByte:#04x},{SecondByte:#04x} : {FieldDesc:s}\n\r"
        Template += "\t{Bus:#04x} : Bus,\n\r"
        Template += "\t{Device:#04x} : Device,\n\r"
        Template += "\t{Function:#04x} : Function."

        Result = Template.format(FirstByte = Frame[0],
                                 SecondByte = Frame[1],
                                 FieldDesc = FieldDesc,
                                 Bus = Frame[0],
                                 Device = (Frame[1] & 0xf8) >> 3,
                                 Function = Frame[1] & 0x7)
    else:
        Result = "Error!!! Invalid BDF length."
                                   
    return Result

def GetMctpPcieVendorId(Frame):
    Template = ""
    Mctp_Vendor_Id = {
    0x1ab4 : 'DMTF'}
    if len(Frame) == 2:
        Template += "{FirstByte:#04x},{SecondByte:#04x} : {VendorIdDesc:s}"
        Result = Template.format(FirstByte = Frame[0],
                                 SecondByte = Frame[1],
                                 VendorIdDesc = Mctp_Vendor_Id.get((Frame[0]<<8) + Frame[1],"Vendor Unknown"))
    else:
        Result = "Error!!! Invalid Vendor ID field length."
                                   
    return Result

def GetMctpMessageCode(Code):
    Mctp_Message_Code = {
    0b01111111 : 'Vendor Defined Type 1'}

    Template = "{MessageCode:#04x} : {MessageCodeDesc:s}"
    Result = Template.format(MessageCode = Code,
                             MessageCodeDesc = Mctp_Message_Code.get(Code,"Message Code Unknown"))
    return Result

def GetMctpPcieVdmRoutingType(RoutingType):
    Mctp_Routing_Type = {
        0b000 : 'Route to Root Complex',
        0b010 : 'Route by ID',
        0b011 : 'Broadcast from Root Complex'}
    return '{Type:#05b} : {Desc}'.format(Type = RoutingType, Desc = Mctp_Routing_Type.get(RoutingType,'Not supported for MCTP'))

def ParseMctpPcieHeader(Header):
    Template = "PCIe Medium-Specific Header: \n\r"
    DataToDisplay = {}

    Template += "{Data[FirstByte]:#04x} : \n\r"
    Template += "\t{Data[RoutingType]:s} : Routing Type,\n\r"

    Template += "{Data[SecondByte]:#04x} : \n\r"
    
    Template += "{Data[ThirdByte]:#04x},{Data[FourthByte]:#04x} : \n\r"
    Template += "\t{Data[Length]:d} : Length of the PCIe VDM Data in Dwords.,\n\r"
    
    Template += "{Data[PciRequesterId]:s}\n\r"
    Template += "{Data[MessageCode]:s} : Message Code,\n\r"
    Template += "{Data[PciTargetId]:s}\n\r"
    Template += "{Data[VendorId]:s} : Vendor Id\n\r"

    DataToDisplay['FirstByte'] = Header[0]
    DataToDisplay['RoutingType']= GetMctpPcieVdmRoutingType(Header[0] & 0x7)
    DataToDisplay['SecondByte'] = Header[1]
    DataToDisplay['ThirdByte'] = Header[2]
    DataToDisplay['FourthByte'] = Header[2]
    DataToDisplay['Length'] = (((Header[2] & 0x3) << 8) + Header[3])
    DataToDisplay['PciRequesterId']= GetMctpPcieBdfAddress(Header[4:6],"PCI Requester ID")
    DataToDisplay['MessageCode']= GetMctpMessageCode(Header[7])
    DataToDisplay['PciTargetId']= GetMctpPcieBdfAddress(Header[8:10],"PCI Target ID")
    DataToDisplay['VendorId']= GetMctpPcieVendorId(Header[10:12])
    
    Result = Template.format(Data = DataToDisplay)
    print(Result)
    return Result


def ParseMctpPcieFrame(PcieFrame):
    #check basic frame size
    if len(PcieFrame) > PCIE_VDM_HEADER_LEN:
        #parse PCIe VDM Header
        ParseMctpPcieHeader(PcieFrame[:12])
        
        #Length of the PCIe VDM Data in bytes
        Length = (((PcieFrame[2] & 0x3) << 8) + PcieFrame[3]) * 4
        PadLen = (PcieFrame[6] & 0x30)>>4
        
        #check PCIe VDM Data Length. PCIe VDM Data starts from 16th byte
        if len(PcieFrame[16:]) == Length:
            MctpFrame = PcieFrame[12:-PadLen]
            #parse MCTP Frame
            MctpParser.ParseMctpFrame(MctpFrame)

            #Add 00h Padding
            print("{Data} : PCIe Medium-Specific Trailer (00h Padding)\n\r".format(Data = ["{Data:#04x}".format(Data = item) for item in PcieFrame[-PadLen:]]))
             
        else:
            print("Error: Invalid MCTP PCIe VDM Data length.")
            print("PCIe VDM Header declares {0} bytes, but frame has {1} bytes.\n\r".format(Length,len(PcieFrame[16:])))
   
    else:
        print("Error: Invalid MCTP PCIe VDM Frame length")
    return


#----Script Start----
if __name__ == "__main__":

    #PcieTstFrame = [0x70, 0x00, 0x10, 0x01, 0x17, 0x00, 0x10, 0x7F, 0x00, 0x00, 0x1A, 0xB4, 0x01, 0x00, 0x00, 0xFB, 0x00, 0x82, 0x0D, 0x00]
    #ParseMctpPcieFrame(PcieTstFrame)
    
    #RoutingTst = 0b000
    #print(GetMctpPcieVdmRoutingType(RoutingTst))
    
    #RoutingTst = 0b010
    #print(GetMctpPcieVdmRoutingType(RoutingTst))
    
    #RoutingTst = 0b011
    #print(GetMctpPcieVdmRoutingType(RoutingTst))
    
    #RoutingTst = 0b111
    #print(GetMctpPcieVdmRoutingType(RoutingTst))

    Mctp_Pcie_Test_Frame = [0x70, 0x00, 0x10, 0x05, 0x02, 0x00, 0x10, 0x7f, 0x00, 0x00, 0x1a, 0xb4, 0x01, 0x50, 0x22, 0xca, 0x7e, 0x80, 0x86, 0xc0, 0x11, 0x00, 0x10, 0x02, 0x00, 0x92, 0x00, 0x03, 0x01, 0xff, 0x22, 0xc8, 0x00, 0x80, 0x0b, 0x00]
    ParseMctpPcieFrame(Mctp_Pcie_Test_Frame)

    Mctp_Pcie_Test_Frame = [0x70, 0x00, 0x10, 0x01, 0x02, 0x00, 0x10, 0x7f, 0x00, 0x00, 0x1a, 0xb4, 0x01, 0x00, 0x22, 0xcc, 0x00, 0x80, 0x02, 0x00]    
    ParseMctpPcieFrame(Mctp_Pcie_Test_Frame)

    Mctp_Pcie_Test_Frame = [0x72, 0x00, 0x10, 0x02, 0x00, 0x92, 0x10, 0x7f, 0x02, 0x00, 0x1a, 0xb4, 0x01, 0x22, 0x50, 0xe4, 0x00, 0x00, 0x02, 0x00, 0x00, 0x11, 0x00, 0x00]    
    ParseMctpPcieFrame(Mctp_Pcie_Test_Frame)

    Mctp_Pcie_Test_Frame = [0x72, 0x00, 0x10, 0x02, 0x00, 0x92, 0x10, 0x7F, 0x01, 0x00, 0x1A, 0xB4, 0x01, 0x50, 0x00, 0xD3, 0x00, 0x17, 0x02, 0x00, 0x00, 0x11, 0x00, 0x00]    
    ParseMctpPcieFrame(Mctp_Pcie_Test_Frame)

    Mctp_Pcie_Test_Frame = [0x72, 0x00, 0x10, 0x02, 0x00, 0x92, 0x10, 0x7F, 0x01, 0x00, 0x1A, 0xB4, 0x01, 0x50, 0x55, 0xF1, 0x00, 0x00, 0x02, 0x00, 0x00, 0x11, 0x00, 0x00]    
    ParseMctpPcieFrame(Mctp_Pcie_Test_Frame)

    Mctp_Pcie_Test_Frame = [0x73, 0x00, 0x10, 0x01, 0x00, 0x92, 0x10, 0x7f, 0x00, 0x00, 0x1a, 0xb4, 0x01, 0xff, 0x50, 0xe8, 0x00, 0x80, 0x0b, 0x00]
    ParseMctpPcieFrame(Mctp_Pcie_Test_Frame)

    Mctp_Pcie_Test_Frame = [0x72, 0x00, 0x10, 0x02, 0x01, 0x02, 0x10, 0x7F, 0x00, 0x92, 0x1A, 0xB4, 0x01, 0x51, 0x61, 0xC3, 0x00, 0x0E, 0x01, 0x00, 0x00, 0x61, 0x00, 0x00]
    ParseMctpPcieFrame(Mctp_Pcie_Test_Frame)

    Mctp_Pcie_Test_Frame = [0x72, 0x00, 0x10, 0x02, 0x00, 0x92, 0x30, 0x7F, 0x01, 0x02, 0x1A, 0xB4, 0x01, 0x00, 0x50, 0xDC, 0x00, 0x8F, 0x01, 0x00, 0x61, 0x00, 0x00, 0x00]
    ParseMctpPcieFrame(Mctp_Pcie_Test_Frame)

    Mctp_Pcie_Test_Frame = [0x72, 0x00, 0x10, 0x01, 0x00, 0x92, 0x10, 0x7F, 0x01, 0x02, 0x1A, 0xB4, 0x01, 0x00, 0x50, 0xE9, 0x00, 0x8C, 0x02, 0x00]
    ParseMctpPcieFrame(Mctp_Pcie_Test_Frame)

    Mctp_Pcie_Test_Frame = [0x72, 0x00, 0x10, 0x02, 0x01, 0x02, 0x10, 0x7F, 0x00, 0x92, 0x1A, 0xB4, 0x01, 0x50, 0x00, 0xC1, 0x00, 0x0C, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00]
    ParseMctpPcieFrame(Mctp_Pcie_Test_Frame)
    
    #print(Mctp_Pcie_Test_Frame)
