# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 20:32:19 2017
@author: M
"""

#MCTP frame parser

Mctp_Message_Types = {
    0x00 : 'MCTP Control',
    0x01 : 'Platform Level Data Model (PLDM)',
    0x02 : 'NC-SI over MCTP',
    0x03 : 'Ethernet over MCTP',
    0x04 : 'NVM Express Management Messages over MCTP',
    0x7e : 'Vendor Defined – PCI',
    0x7f : 'Vendor Defined – IANA'}

Mctp_Control_Message_Command_Codes = {
    0x00 : 'Reserved',
    0x01 : 'Set Endpoint EID',
    0x02 : 'Get Endpoint EID',
    0x03 : 'Get Endpoint UUID',
    0x04 : 'Get MCTP Version Support',
    0x05 : 'Get Message Type Support',
    0x06 : 'Get Vendor Defined Message Support',
    0x07 : 'Resolve Endpoint ID',
    0x08 : 'Allocate Endpoint IDs',
    0x09 : 'Routing Information Update',
    0x0a : 'Get Routing Table Entries',
    0x0b : 'Prepare for Endpoint Discovery',
    0x0c : 'Endpoint Discovery',
    0x0d : 'Discovery Notify',
    0x0e : 'Get Network ID',
    0x0f : 'Query Hop'}
   
Mctp_Control_Message_Status_Codes = {
    0x00 : 'SUCCESS',
    0x01 : 'ERROR',
    0x02 : 'ERROR_INVALID_DATA',
    0x03 : 'ERROR_INVALID_LENGTH',
    0x04 : 'ERROR_NOT_READY',
    0x05 : 'ERROR_UNSUPPORTED_CMD'}

Mctp_Physical_Transport_Bindings = {
    0x00 : 'Reserved',
    0x01 : 'MCTP over SMBus',
    0x02 : 'MCTP over PCIe VDM',
    0x03 : 'MCTP over USB',
    0x04 : 'MCTP over KCS',
    0x05 : 'MCTP over Serial',
    0xff : 'Vendor Defined'}

Mctp_Physical_Medium_Identifiers = {
    0x00 : 'Unspecified',
    0x01 : 'SMBus 2.0 100 kHz compatible',
    0x02 : 'SMBus 2.0 + I2C 100 kHz compatible',
    0x03 : 'I2C 100 kHz compatible (Standard-mode)',
    0x04 : 'I2C 400 kHz compatible (Fast-mode)',
    0x05 : 'I2C 1 MHz compatible (Fast-mode Plus)',
    0x06 : 'I2C 3.4 MHz compatible (High-speed mode)',
    0x07 : 'Reserved',
    0x08 : 'PCIe 1.1 compatible',
    0x09 : 'PCIe 2.0 compatible',
    0x0a : 'PCIe 2.1 compatible',
    0x0b : 'PCIe 3.0 compatible',
    0x0c : 'Reserved',
    0x0d : 'Reserved',
    0x0e : 'Reserved',
    0x0f : 'PCI compatible (PCI 1.0,2.0,2.1,2.2,2.3,3.0,PCI-X 1.0, PCI-X 2.0)',
    0x10 : 'USB 1.1 compatible',
    0x11 : 'USB 2.0 compatible',
    0x12 : 'USB 3.0 compatible',
    0x13 : 'Reserved',
    0x14 : 'Reserved',
    0x15 : 'Reserved',
    0x16 : 'Reserved',
    0x17 : 'Reserved',
    0x18 : 'NC-SI over RBT',
    0x20 : 'KCS / Legacy (Fixed Address Decoding)',
    0x21 : 'KCS / PCI (Base Class 0xC0 Subclass 0x01)',
    0x22 : 'Serial Host / Legacy (Fixed Address Decoding)',
    0x23 : 'Serial Host2 / PCI (Base Class 0x07 Subclass 0x00)',
    0x24 : 'Asynchronous Serial3 (Between MCs and IMDs)'}



def GetMctpControlMessageCommandCode(CmdCode):
    return '{Code:#04x} : {Desc}'.format(Code = CmdCode, Desc = Mctp_Control_Message_Command_Codes.get(CmdCode,'Transport Specific Command Code'))
   
def GetMctpControlMessageCommandName(CmdCode):
    return Mctp_Control_Message_Command_Codes.get(CmdCode,'Reserved')
   
def GetMctpMessageType(TypeCode):
    return Mctp_Message_Types.get(TypeCode,'Reserved')
    

def GetSetEndpointEidOperationName(Oper):
   
    return


#0x01 : 'Set Endpoint EID'
def ParseMctpSetEndpointEidReq(Frame):
    Template = ""
    if len(Frame) == 2:

        Mctp_Set_Endpoint_Eid_Operation = {
            0b00 : 'Set EID',
            0b01 : 'Force EID',
            0b10 : 'Reset EID (optional)',
            0b11 : 'Set Discovered Flag'}
       
        Template += "{Operation:#04x} : {rsvd:#b}=Reserved, {Oper:#04b}={OperDesc:s},\n\r"
        Template += "{EndpointID:#04x} : Endpoint ID \n\r"

        Result = Template.format(Operation = Frame[0],
                                 rsvd = (Frame[0] & 0xfc) >> 2,
                                 Oper = Frame[0] & 0x3,
                                 OperDesc = Mctp_Set_Endpoint_Eid_Operation.get(Frame[0] & 0x3,'Error unknown Operation Code'),
                                 EndpointID = Frame[1])
       
    else:
       Result = Template + "Error Invalid length"
    return Result

def ParseMctpSetEndpointEidRes(Frame):
    Template = ""
    if len(Frame) == 4:
        Mctp_Set_Endpoint_Eid_Assignment_Status= {
            0b00 : 'EID assignment accepted',
            0b01 : 'EID assignment rejected',
            0b10 : 'reserved',
            0b11 : 'reserved'}
        Mctp_Set_Endpoint_Eid_Allocation_Status= {
            0b00 : 'Device does not use an EID pool',
            0b01 : 'Endpoint requires EID pool allocation',
            0b10 : 'Endpoint uses an EID pool and has already received an allocation for that pool',
            0b11 : 'reserved'}
       
        Template += "{CompCode:#04x} : {CompCodeDesc:s},\n\r"
        Template += "{SecondByte:#04x} : {rsvd1:#04b}=reserved, {EidAssignStatus:#04b}={EidAssignDesc:s}, {rsvd2:#04b}=reserved, {EidAllocStatus:#04b}={EidAllocDesc:s},\n\r"
        Template += "{EidSetting:#04x} : EID Setting,\n\r"
        Template += "{EidPoolSize:#04x} : EID Pool Size,\n\r"

     
        Result = Template.format(CompCode = Frame[0],
                                 CompCodeDesc = Mctp_Control_Message_Status_Codes.get(Frame[0]),
                                 SecondByte = Frame[1],
                                 rsvd1 = (Frame[1] & 0xc0) >> 6,
                                 EidAssignStatus = (Frame[1] & 0x30) >> 4,
                                 EidAssignDesc = Mctp_Set_Endpoint_Eid_Assignment_Status.get((Frame[1] & 0x30) >> 4, "Error unknown EID Assignment Status"),
                                 rsvd2 = (Frame[1] & 0x0c) >> 2,
                                 EidAllocStatus = Frame[1] & 0x03,
                                 EidAllocDesc = Mctp_Set_Endpoint_Eid_Allocation_Status.get(Frame[1] & 0x03, "Error unknown EID Allocation Status"),
                                 EidSetting = Frame[2],
                                 EidPoolSize = Frame[3])
                               

    else:
        Result = Template + "Error Invalid length"   
    return Result


#0x02 : 'Get Endpoint EID'
def ParseMctpGetEndpointEidReq(Frame):
    Template = ""
    if not Frame:
        Result = ""
    else:
        Template += str(["{Item:#04x}".format(Item = ii) for ii in Frame])
        Result = Template + " : Error!!! Unexpected data\n\r"
    return Result


def ParseMctpGetEndpointEidRes(Frame):
    Template = ""
    if len(Frame) == 4:
        Mctp_Get_Endpoint_Type= {
            0b00 : 'simple endpoint',
            0b01 : 'bus owner/bridge',
            0b10 : 'reserved',
            0b11 : 'reserved'}
        Mctp_Get_Endpoint_Id_Type= {
            0b00 : 'dynamic EID',
            0b01 : 'static EID supported. The endpoint was configured with a static EID.',
            0b10 : 'static EID supported. Present EID matches static EID',
            0b11 : 'static EID supported. Present EID does not match static EID'}

        Template += "{CompCode:#04x} : {CompCodeDesc:s},\n\r"
        Template += "{EndpointID:#04x} : Endpoint ID,\n\r"
        Template += "{ThirdByte:#04x} : {rsvd1:#04b}=reserved, {EndType:#04b}={EndTypeDesc:s}, {rsvd2:#04b}=reserved, {EndIdType:#04b}={EndIdTypeDesc:s} \n\r"
        Template += "{MediumSpecific:#04x} : Medium-Specific Information\n\r"

        Result = Template.format(CompCode = Frame[0],
                                 CompCodeDesc = Mctp_Control_Message_Status_Codes.get(Frame[0]),
                                 EndpointID = Frame[1],
                                 ThirdByte = Frame[2],
                                 rsvd1 = (Frame[2] & 0xc0) >>6,
                                 EndType =  (Frame[2] & 0x30) >>4,
                                 EndTypeDesc = Mctp_Get_Endpoint_Type.get((Frame[2] & 0x30) >>4, 'Error Unknown Endpoint Type'),
                                 rsvd2 = (Frame[2] & 0x0c) >>2,
                                 EndIdType = Frame[2] & 0x03,
                                 EndIdTypeDesc = Mctp_Get_Endpoint_Id_Type.get(Frame[2] & 0x03, 'Error Unknown Endpoint ID Type' ),
                                 MediumSpecific = Frame[3])
       
    else:
        Result = Template + "Error Invalid length"   
    return Result
       
   
#0x03 : 'Get Endpoint UUID'
def ParseMctpGetEndpointUuidReq(Frame):
    Template = ""
    if not Frame:
        Result = ""
    else:
        Template += str(["{Item:#04x}".format(Item = ii) for ii in Frame])
        Result = Template + " : Error!!! Unexpected data\n\r"
    return Result

def ParseMctpGetEndpointUuidRes(Frame):
    ...
    return ""
       
#0x04 : 'Get MCTP Version Support',
def ParseMctpGetMctpVersionSupportReq(Frame):
    ...
    return ""
def ParseMctpGetMctpVersionSupportRes(Frame):
    ...
    return ""

#0x05 : 'Get Message Type Support',
def ParseMctpGetMessageTypeSupportReq(Frame):
    Template = ""
    if not Frame:
        Result = ""
    else:
        Template += str(["{Item:#04x}".format(Item = ii) for ii in Frame])
        Result = Template + " : Error!!! Unexpected data\n\r"
    return Result


def ParseMctpGetMessageTypeSupportRes(Frame):
    Template = ""
    try:
        Message_Type_Count = Frame[1]
        Frame_Expected_Length = Message_Type_Count + 2; #2 first two bytes of response
       
        if len(Frame) == Frame_Expected_Length:
            Template += "{CompCode:#04x} : {CompCodeDesc:s},\n\r"
            Template += "{MsgTypeCount:#04x} : MCTP Message Type Count,\n\r"
            #list supported message types
            for MsgType in Frame[2:]:
                Template += "{MsgTypeVar:#04x} : Supported - {MsgTypeDesc:s}\n\r".format(MsgTypeVar = MsgType,
                                                                         MsgTypeDesc = GetMctpMessageType(MsgType))

            Result = Template.format(CompCode = Frame[0],
                                     CompCodeDesc = Mctp_Control_Message_Status_Codes.get(Frame[0]),
                                     MsgTypeCount = Frame[1])
       
        else:
            Result = Template + "Error!!! Frame length different than expected"
       
    except:
        Result = Template + "Error!!! Invalid length"

    return Result


#0x06 : 'Get Vendor Defined Message Support',
def ParseMctpGetVendorDefinedMessageSupportReq(Frame):
    Template = ""

    if len(Frame) == 1:
        Template += "{VendorIdSel:#04x} : Vendor ID Set Selector\n\r"
       
        Result = Template.format(VendorIdSel = Frame[0])
    else:
       Result = Template + "Error!!! Invalid length"
    return Result

def ParseMctpGetVendorDefinedMessageSupportRes(Frame):
    Template = ""

    Mctp_Vendor_Id_Sel= {
        0xff : 'No more capability sets'}
   
    Mctp_Vendor_Id_Format = {
        0x00 : {"Name" : "PCI Vendor ID", "Length" : 2},
        0x01 : {"Name" : "IANA Enterprise Number", "Length" : 4}
        }

    #<TODO>: calculate frame length
    if len(Frame) > 5:
             
        Template += "{CompCode:#04x} : {CompCodeDesc:s},\n\r"
        Template += "{VendorIdSel:#04x} : {VendorIdSelDesc:s}\n\r"
        Template += "{VendorIdFormat:#04x} : {VendorIdFormatDesc:s}\n\r"
        Template += str(["{Item:#04x}".format(Item = ii) for ii in Frame[3:-2]]) + " : Vendor ID\n\r"
        Template += "{CmdSetType1:#04x} {CmdSetType2:#04x} : Command Set Type\n\r"
     
        Result = Template.format(CompCode = Frame[0],
                                 CompCodeDesc = Mctp_Control_Message_Status_Codes.get(Frame[0]),
                                 VendorIdSel = Frame[1],
                                 VendorIdSelDesc = Mctp_Vendor_Id_Sel.get(Frame[1],'Vendor ID Set Selector'),
                                 VendorIdFormat = Frame[2],
                                 VendorIdFormatDesc = (Mctp_Vendor_Id_Format.get(Frame[2],'Error!!! Unknown Vendor ID Format')).get("Name"),
                                 CmdSetType1 = Frame[-2],
                                 CmdSetType2 = Frame[-1])
                                

    else:
        Result = Template + "Error Invalid length"   
    return Result

#0x07 : 'Resolve Endpoint ID',
#0x08 : 'Allocate Endpoint IDs',
#0x09 : 'Routing Information Update',

#0x0a : 'Get Routing Table Entries',
def ParseMctpGetRoutingTableReq(Frame):
    Template = ""
    if len(Frame) == 1:
        Template += "{EntryHandle:#04x} : Entry Handle\n\r"
       
        Result = Template.format(EntryHandle = Frame[0])
    else:
       Result = Template + "Error!!! Invalid length"
    return Result


def GetEntryLength(Frame):
    try:
        EntryLength =  6 + Frame[5]
        return EntryLength
    except:
        return 0

def ParsePciePhysicalAddress(Address):
    Template = ""
    Template += str(["{Item:#04x}".format(Item = ii) for ii in Address]) + " : PCIe Address = "
    Template += "{Bus:02x}:Bus, "
    Template += "{Dev:02x}:Device, "
    Template += "{Func:02x}:Function\n\r"

    Result = Template.format(Bus = Address[0],
                             Dev = (Address[1]& 0xc0) >> 3,
                             Func = Address[1]& 0x07)
   
    return Result

Mctp_Physical_Address_Parsers = {
    0x00 : None,
    0x01 : None,
    0x02 : ParsePciePhysicalAddress,
    0x03 : None,
    0x04 : None,
    0x05 : None,
    0xff : None}

def ParsePhysicalAddress(TransportBinding,Address):
    Parser = Mctp_Physical_Address_Parsers.get(TransportBinding,None)
    if None != Parser:
        return Parser(Address)
    else:
        return "Error!!! Unknown physical address parser"

def ParseGetRoutingEntry(Entry):
    Mctp_Entry_Type = {
        0b00 : 'Single Endpoint that does not operate as an MCTP bridge',
        0b01 : 'EID range for a bridge where the starting EID is the EID of the bridge...',
        0b10 : 'Single endpoint that serves as an MCTP bridge',
        0b11 : 'EID range for a bridge, but does not include the EID of the bridge itself'
        }
    Mctp_DynStat_Entry = {
        0b0 : 'Entry was dynamically created ',
        0b1 : 'Entry was statically configured'
        }
   
    Template = ""
    Template += "{SizeEidRange:#04x} : Size of EID range associated with this entry\n\r"
    Template += "{StartingEid:#04x} : Starting EID\n\r"
    Template += "{Byte3:#04x} : Entry Type/Port Number:\n\r"
    Template += "\t{EntryType:#02b} : {EntryTypeDesc:s}\n\r"
    Template += "\t{DynStatEntry:#01b} : {DynStatEntryDesc:s}\n\r"
    Template += "\t{PortNumber:#04x} : Port Number\n\r"
    Template += "{PhyTransBinding:#04x} : Physical Transport Binding - {PhyTransBindingDesc:s}\n\r"
    Template += "{PhyMediaId:#04x} : Physical Medium - {PhyMediaIdDesc:s}\n\r"
    Template += "{PhyAddrSize:#04x} : Physical Address Size\n\r"
    Template += ParsePhysicalAddress(Entry[3],Entry[6:])

    Result = Template.format(SizeEidRange = Entry[0],
                             StartingEid = Entry[1],
                             Byte3 = Entry[2],
                             EntryType = (Entry[2] & 0xc0) >> 6,
                             EntryTypeDesc = Mctp_Entry_Type.get((Entry[2] & 0xc0) >> 6, 'Error!!! Unknown Entry Type'),
                             DynStatEntry = (Entry[2] & 0x20) >> 5,
                             DynStatEntryDesc = Mctp_DynStat_Entry.get((Entry[2] & 0x20) >> 5,'Error!!! Unknown Dynamic or Static Type'),
                             PortNumber = (Entry[2] & 0x1f),
                             PhyTransBinding = Entry[3],
                             PhyTransBindingDesc = Mctp_Physical_Transport_Bindings.get(Entry[3],'Reserved'),
                             PhyMediaId =  Entry[4],
                             PhyMediaIdDesc = Mctp_Physical_Medium_Identifiers.get(Entry[4],'Reserved'),
                             PhyAddrSize = Entry[5])
    return Result
   
def ParseMctpGetRoutingTableRes(Frame):
    Template = ""

    Mctp_Entry_Handle= {
        0xff : 'No more entries'}
   
    Mctp_Frame_Length = len(Frame)
    Mctp_Frame_Expected_Length = 0
   
    #The Frame length shall have at minimum 3 bytes (3 common data bytes)
    if Mctp_Frame_Length >= 3:
        Mctp_Frame_Expected_Length = 3
        Mctp_Entries_Count = Frame[2]
        GetRoutingTableEntries = []

        StartIndex = 3 #index of first Entry in Routing Table
        for ii in range(Mctp_Entries_Count):
            EntryLength = GetEntryLength(Frame[StartIndex:])
            if EntryLength:
                Mctp_Frame_Expected_Length += EntryLength
                GetRoutingTableEntries.append(Frame[StartIndex:StartIndex+EntryLength])
                StartIndex += EntryLength
            else:
                Mctp_Frame_Expected_Length = 0
                break
    
        if Mctp_Frame_Length == Mctp_Frame_Expected_Length:
            Template += "{CompCode:#04x} : {CompCodeDesc:s},\n\r"
            Template += "{NextEntryHandle:#04x} : {NextEntryHandleDesc:s},\n\r"
            Template += "{EntriesCount:#04x} : Entries Count in this response,\n\r"
            for Entry in GetRoutingTableEntries:
                Template += ParseGetRoutingEntry(Entry)
       
            Result = Template.format(CompCode = Frame[0],
                                     CompCodeDesc = Mctp_Control_Message_Status_Codes.get(Frame[0]),
                                     NextEntryHandle = Frame[1],
                                     NextEntryHandleDesc = Mctp_Entry_Handle.get(Frame[1],'Next Entry Handle'),
                                     EntriesCount = Frame[2])
        else:
            Result = Template + "Error!!! Frame length different than expected"

    else:
        Result = Template + "Error!!! Invalid frame length"
   
    return Result


#0x0b : 'Prepare for Endpoint Discovery',
def ParseMctpPrepareForEndpointDiscoveryReq(Frame):
    Template = ""
    if not Frame:
        Result = ""
    else:
        Template += str(["{Item:#04x}".format(Item = ii) for ii in Frame])
        Result = Template + " : Error!!! Unexpected data\n\r"
    return Result
   
def ParseMctpPrepareForEndpointDiscoveryRes(Frame):
    Template = ""
    if len(Frame) == 1:
        Template += "{CompCode:#04x} : {CompCodeDesc:s},\n\r"
       
        Result = Template.format(CompCode = Frame[0],
                                 CompCodeDesc = Mctp_Control_Message_Status_Codes.get(Frame[0]))
       
    else:
        Result = Template + "Error Invalid length"
    return Result
   
#0x0c : 'Endpoint Discovery',
def ParseMctpEndpointDiscoveryReq(Frame):
    Template = ""
    if not Frame:
        Result = ""
    else:
        Template += str(["{Item:#04x}".format(Item = ii) for ii in Frame])
        Result = Template + " : Error!!! Unexpected data\n\r"
    return Result
   
def ParseMctpEndpointDiscoveryRes(Frame):
    Template = ""
    if len(Frame) == 1:
        Template += "{CompCode:#04x} : {CompCodeDesc:s},\n\r"
       
        Result = Template.format(CompCode = Frame[0],
                                 CompCodeDesc = Mctp_Control_Message_Status_Codes.get(Frame[0]))
       
    else:
        Result = Template + "Error Invalid length"
    return Result

#0x0d : 'Discovery Notify',
def ParseMctpDiscoveryNotifyReq(Frame):
    Template = ""
    if not Frame:
        Result = ""
    else:
        Template += str(["{Item:#04x}".format(Item = ii) for ii in Frame])
        Result = Template + " : Error!!! Unexpected data\n\r"
    return Result
   
def ParseMctpDiscoveryNotifyRes(Frame):
    Template = ""
    if len(Frame) == 1:
        Template += "{CompCode:#04x} : {CompCodeDesc:s},\n\r"
       
        Result = Template.format(CompCode = Frame[0],
                                 CompCodeDesc = Mctp_Control_Message_Status_Codes.get(Frame[0]))
       
    else:
        Result = Template + "Error!!! Invalid length"
    return Result


#0x0e : 'Get Network ID',
def ParseMctpGetNetworkIdReq(Frame):
    ...
    return ""
   
def ParseMctpGetNetworkIdRes(Frame):
    ...
    return ""


#0x0f : 'Query Hop'}


Mctp_Control_Message_Handlers = {
    0x00 : {'Req' : None, 'Res': None},
    0x01 : {'Req' : ParseMctpSetEndpointEidReq, 'Res': ParseMctpSetEndpointEidRes}, #Done
    0x02 : {'Req' : ParseMctpGetEndpointEidReq, 'Res': ParseMctpGetEndpointEidRes}, #Done
    0x03 : {'Req' : ParseMctpGetEndpointUuidReq, 'Res': ParseMctpGetEndpointUuidRes},
    0x04 : {'Req' : ParseMctpGetMctpVersionSupportReq, 'Res': ParseMctpGetMctpVersionSupportRes},
    0x05 : {'Req' : ParseMctpGetMessageTypeSupportReq, 'Res': ParseMctpGetMessageTypeSupportRes}, #Done
    0x06 : {'Req' : ParseMctpGetVendorDefinedMessageSupportReq, 'Res': ParseMctpGetVendorDefinedMessageSupportRes}, #Done + 1 TODO
    0x07 : {'Req' : None, 'Res': None},
    0x08 : {'Req' : None, 'Res': None},
    0x09 : {'Req' : None, 'Res': None},
    0x0a : {'Req' : ParseMctpGetRoutingTableReq, 'Res': ParseMctpGetRoutingTableRes}, #Done
    0x0b : {'Req' : ParseMctpPrepareForEndpointDiscoveryReq, 'Res': ParseMctpPrepareForEndpointDiscoveryRes}, #Done
    0x0c : {'Req' : ParseMctpEndpointDiscoveryReq, 'Res': ParseMctpEndpointDiscoveryRes}, #Done
    0x0d : {'Req' : ParseMctpDiscoveryNotifyReq, 'Res': ParseMctpDiscoveryNotifyRes}, #Done
    0x0e : {'Req' : ParseMctpGetNetworkIdReq, 'Res': ParseMctpGetNetworkIdRes},
    0x0f : {'Req' : None, 'Res': None}
    }


def GetMctpControlFramePayloadParser(RqBit,CmdCode):
    Parser_Function_Handler = None
    Parser_Function_Dict = Mctp_Control_Message_Handlers.get(CmdCode,None)
    if None != Parser_Function_Dict:
        if RqBit:
            Parser_Function_Handler = Parser_Function_Dict.get('Req')
        else:
            Parser_Function_Handler = Parser_Function_Dict.get('Res')
       
    return Parser_Function_Handler


def ParseMctpControlFrameCommonHeader(Frame):
    Template =  "\n\r"
    Template += "{FirstByte:#04x} : {IC:#03b}=IC, 0x00=MCTP Control Command,\n\r"
    Template += "{SecondByte:#04x} : {Rq:#03b}=Rq, {D:#03b}=D, {rsvd:#03b}=rsvd, {InsID:#d} : Instance ID \n\r"
    Template += "{CommandCode:#04x} : {CommandDesc:s} \n\r"

    Result = Template.format(FirstByte = Frame[0],
                             IC = (Frame[0] & 0x80) >>7,
                             SecondByte = Frame[1],
                             Rq = (Frame[1] & 0x80) >>7,
                             D = (Frame[1] & 0x40) >> 6,
                             rsvd = (Frame[1] & 0x20) >> 5,
                             InsID = (Frame[1] & 0x1f),
                             CommandCode = Frame[2],
                             CommandDesc = GetMctpControlMessageCommandName(Frame[2]))

    return Result


def ParseMctpControlFrame(Frame):
    Template = "MCTP Control Frame: "
    if len(Frame) >= 3:
        RqBit = (Frame[1] & 0x80) >>7

        Template += ParseMctpControlFrameCommonHeader(Frame[0:3])

        MctpControlFramePayloadParser = GetMctpControlFramePayloadParser(RqBit,Frame[2])
        if None != MctpControlFramePayloadParser:
            Template += MctpControlFramePayloadParser(Frame[3:])
        else:
            Template += "\n\r No parser found"

        Result = Template.format()
    else:
        Result = Template + "Error Invalid length"

    print(Result)
    return Result

def ParseMctpVendorDefinedPcieFrame(Packet_Data):
    ...
    return


def ParseMctpPacketPayload(Packet_Data):
    Msg_Type = Packet_Data[0] & 0x7f
    if 0x00 == Msg_Type:
        ParseMctpControlFrame(Packet_Data)
    elif 0x7e == Msg_Type:
        ParseMctpVendorDefinedPcieFrame(Packet_Data)
    else:
        print("Parser unsupported message type")
    return


def ParseMctpTransportHeader(Header):
    Template = "MCTP Transport Header:"
    if len(Header) == 4:
        Template += "\n\r"
        Template += "{FirstByte:#04x} : {Rsvd:#x} : Reserved, {Head_Ver:#x} : Header Version,\n\r"
        Template += "{Dest_Eid:#04x} : Destination endpoint ID,\n\r"
        Template += "{Src_Eid:#04x} : Source endpoint ID,\n\r"
        Template += "{ForthByte:#04x} : {SOM:#03b}=SOM, {EOM:#03b}=EOM, {PktSeq:#d}=PktSeq#, {TO:#03b}=TO, {MsgTag:#d}=MsgTag"
       
        Result = Template.format(FirstByte = Header[0],
                        Rsvd= Header[0]>>4,
                        Head_Ver = Header[0] & 0x0f,
                        Dest_Eid = Header[1],
                        Src_Eid = Header[2],
                        ForthByte = Header[3],
                        SOM = (Header[3] & 0x80)>>7,
                        EOM = (Header[3] & 0x40)>>6,
                        PktSeq = (Header[3] & 0x30)>>4,
                        TO = (Header[3] & 0x8)>>3,
                        MsgTag = (Header[3] & 0x7))
      
    else:
        Result =Template + "Error Invalid length"
       
    print(Result)  
    return Result


def ParseMctpFrame(Frame):
    if len(Frame) >= 5:
        #<TODO:>PrintMctpFrame(Frame)
        ParseMctpTransportHeader(Frame[:4])
        ParseMctpPacketPayload(Frame[4:])
    else:
        print("Invalid MCTP Frame length")
    return

#----Script Start----
if __name__ == "__main__":

# 0x70 0x00 0x10 0x01 0x17 0x00 0x10 0x7F 0x00 0x00 0x1A 0xB4 0x01 0x00 0x00 0xFB 0x00 0x82 0x0D     req0D discovery notify
# 0x70 0x00 0x10 0x01 0x17 0x00 0x10 0x7F 0x00 0x00 0x1A 0xB4 0x01 0x00 0x00 0xD9 0x00 0x87 0x02     req02 Get Endpoint EID

    #Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x01, 0x00, 0x60]    #Set EID Req
    #ParseMctpFrame(Mctp_Test_Frame)

    #Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x01, 0x00, 0x00, 0x60, 0x03]    #Set EID Res
    #ParseMctpFrame(Mctp_Test_Frame)

    #Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x02]    #Get EID Req
    #ParseMctpFrame(Mctp_Test_Frame)

    #Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x02, 0x00, 0x61, 0x00, 0x00]    #Get EID Res
    #ParseMctpFrame(Mctp_Test_Frame)

    #Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x06, 0x01]    #0x06 Req VDM Support Req
    #ParseMctpFrame(Mctp_Test_Frame)

    #Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x06, 0x00, 0xff, 0x01, 0x80, 0x86, 0x00, 0x00]    #Get EID Res
    #ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x05, 0x00, 0x02, 0x00, 0x7e]    #0x05 Get Message Type Support res
    ParseMctpFrame(Mctp_Test_Frame)

    #Mctp_Test_Frame = [0x01, 0x60, 0x50, 0xC0, 0x00, 0x00, 0x0A, 0x00, 0xFF, 0x02, 0x01, 0x60, 0x00, 0x02, 0x08, 0x02, 0x01, 0x00, 0x01, 0x61, 0x00, 0x02, 0x08, 0x02, 0x18, 0x00]
    #ParseMctpFrame(Mctp_Test_Frame)

    #print(MctpTestTransportHeader)
    #print(ParseMctpTransportHeader(MctpTestTransportHeader))
    #print(GetMctpControlMessageCommandCode(0x00))
    #print(GetMctpControlMessageCommandCode(0x01))
    #print(GetMctpControlMessageCommandCode(0x02))
    #print(GetMctpControlMessageCommandCode(0x1f))
    #print("")
    #print(ParseMctpTransportHeader([0x11,0x12,0x13]))
    #print(ParseMctpTransportHeader([0xf1,0x11,0x12,0x13]))
    #print("")
    #print(ParseMctpControlFrame([0xf1,0x11,0x02,0x00]))