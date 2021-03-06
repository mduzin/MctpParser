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

Mctp_Eid_Values = {
    0x01 : 'Reserved',
    0x02 : 'Reserved',
    0x03 : 'Reserved',
    0x04 : 'Reserved',
    0x05 : 'Reserved',
    0x06 : 'Reserved',
    0x07 : 'Reserved',
    0xFF : 'Broadcast EID'}

Mctp_Source_Eid_Values = {}
Mctp_Source_Eid_Values.update(Mctp_Eid_Values)
Mctp_Source_Eid_Values[0x00] = "Null Source EID"

Mctp_Destination_Eid_Values = {}
Mctp_Destination_Eid_Values.update(Mctp_Eid_Values)
Mctp_Destination_Eid_Values[0x00] = "Null Destination EID"

#Global values
SUCCESS = 0x00


def GetMctpControlMessageCommandCode(CmdCode):
    return '{Code:#04x} : {Desc}'.format(Code = CmdCode, Desc = Mctp_Control_Message_Command_Codes.get(CmdCode,'Transport Specific Command Code'))
   
def GetMctpControlMessageCommandName(CmdCode):
    return Mctp_Control_Message_Command_Codes.get(CmdCode,'Reserved')
   
def GetMctpMessageType(TypeCode):
    return Mctp_Message_Types.get(TypeCode,'Reserved')

def GetMctpEidDesc(Eid,Dict=Mctp_Eid_Values,Default="Eid Value"):
    return Dict.get(Eid,Default)

def GetMctpDestEidDesc(Eid):
    return GetMctpEidDesc(Eid,Mctp_Destination_Eid_Values)

def GetMctpSrcEidDesc(Eid):
    return GetMctpEidDesc(Eid,Mctp_Source_Eid_Values)

#0x01 : 'Set Endpoint EID'
def ParseMctpSetEndpointEidReq(Frame):
    Template = ""
    if len(Frame) == 2:

        Mctp_Set_Endpoint_Eid_Operation = {
            0b00 : 'Set EID',
            0b01 : 'Force EID',
            0b10 : 'Reset EID (optional)',
            0b11 : 'Set Discovered Flag'}
       
        Template += "{Operation:#04x} : Operation \n\r" 
        Template += "\t{rsvd:#b} : Reserved, \n\r"
        Template += "\t{Oper:#04b} : {OperDesc:s} : Operation.\n\r"
        Template += "{EndpointID:#04x} : Endpoint ID \n\r"

        Result = Template.format(Operation = Frame[0],
                                 rsvd = (Frame[0] & 0xfc) >> 2,
                                 Oper = Frame[0] & 0x3,
                                 OperDesc = Mctp_Set_Endpoint_Eid_Operation.get(Frame[0] & 0x3,'Error!!! unknown Operation Code'),
                                 EndpointID = Frame[1])
       
    else:
       Result = Template + "Error Invalid length"
    return Result

def ParseMctpSetEndpointEidRes(Frame):
    Template = ""
    DataToDisplay = {}

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

    #Completion Code
    Template += "{Data[CompCode]:#04x} : {Data[CompCodeDesc]:s} : Completion Code\n\r"
    DataToDisplay['CompCode']= Frame[0]
    DataToDisplay['CompCodeDesc'] = Mctp_Control_Message_Status_Codes.get(Frame[0])

    #Successful response 
    if SUCCESS == Frame[0]:
        #...with valid payload length
        if len(Frame[1:]) == 3:
            Template += "{Data[SecondByte]:#04x} : \n\r"
            Template += "\t{Data[rsvd1]:#04b} : Reserved, \n\r"
            Template += "\t{Data[EidAssignStatus]:#04b} : {Data[EidAssignDesc]:s} : EID Assignment status,\n\r"
            Template += "\t{Data[rsvd2]:#04b} : Reserved,\n\r"
            Template += "\t{Data[EidAllocStatus]:#04b} : {Data[EidAllocDesc]:s} : EID allocation status.\n\r"
            Template += "{Data[EidSetting]:#04x} : EID Setting,\n\r"
            Template += "{Data[EidPoolSize]:#04x} : EID Pool Size,\n\r"
      
            DataToDisplay['SecondByte'] = Frame[1]
            DataToDisplay['rsvd1'] = (Frame[1] & 0xc0) >> 6
            DataToDisplay['EidAssignStatus'] = (Frame[1] & 0x30) >> 4
            DataToDisplay['EidAssignDesc'] = Mctp_Set_Endpoint_Eid_Assignment_Status.get((Frame[1] & 0x30) >> 4, "Error unknown EID Assignment Status")
            DataToDisplay['rsvd2'] = (Frame[1] & 0x0c) >> 2
            DataToDisplay['EidAllocStatus'] = Frame[1] & 0x03
            DataToDisplay['EidAllocDesc'] = Mctp_Set_Endpoint_Eid_Allocation_Status.get(Frame[1] & 0x03, "Error unknown EID Allocation Status")
            DataToDisplay['EidSetting'] = Frame[2]
            DataToDisplay['EidPoolSize'] = Frame[3]
            
        #...with invalid payload length
        elif len(Frame[1:]) > 0:
            Template += "{Data[InvalidPayload]} : Error!!! Invalid payload length\n\r"

            DataToDisplay['InvalidPayload'] = [hex(item) for item in Frame[1:]]  #Invalid payload

        #...with no payload
        else:
            Template += "Error!!! No payload\n\r"
            

    #Unsuccesful response "SUCCESS != Frame[0]:"
    else:
        #...with unexpected payload
        if len(Frame[1:]) > 0:
            Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"

            DataToDisplay['UnexpectedData'] = [hex(item) for item in Frame[1:]] #Unexpected data

    Result = Template.format(Data = DataToDisplay) 
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
    DataToDisplay = {}

    Mctp_Get_Endpoint_Type= {
        0b00 : 'simple endpoint',
        0b01 : 'bus owner/bridge',
        0b10 : 'reserved',
        0b11 : 'reserved'}
    Mctp_Get_Endpoint_Id_Type= {
        0b00 : 'dynamic EID',
        0b01 : 'static EID supported.',
        0b10 : 'static EID supported. Present EID matches static EID',
        0b11 : 'static EID supported. Present EID does not match static EID'}

    #Completion Code
    Template += "{Data[CompCode]:#04x} : {Data[CompCodeDesc]:s} : Completion Code\n\r"
    DataToDisplay['CompCode']= Frame[0]
    DataToDisplay['CompCodeDesc'] = Mctp_Control_Message_Status_Codes.get(Frame[0])

    #Successful response 
    if SUCCESS == Frame[0]:
        #...with valid payload length
        if len(Frame[1:]) == 3:
            Template += "{Data[EndpointID]:#04x} : Endpoint ID\n\r"
            Template += "{Data[ThirdByte]:#04x} : Endpoint Type\n\r"
            Template += "\t{Data[rsvd1]:#04b} : Reserved,\n\r"
            Template += "\t{Data[EndType]:#04b} : {Data[EndTypeDesc]:s},\n\r"
            Template += "\t{Data[rsvd2]:#04b} : Eeserved,\n\r"
            Template += "\t{Data[EndIdType]:#04b} : {Data[EndIdTypeDesc]:s}. \n\r"
            Template += "{Data[MediumSpecific]:#04x} : Medium-Specific Information\n\r"

            DataToDisplay['EndpointID'] = Frame[1]
            DataToDisplay['ThirdByte'] = Frame[2]
            DataToDisplay['rsvd1'] = (Frame[2] & 0xc0) >>6
            DataToDisplay['EndType'] = (Frame[2] & 0x30) >>4
            DataToDisplay['EndTypeDesc'] = Mctp_Get_Endpoint_Type.get((Frame[2] & 0x30) >>4, 'Error Unknown Endpoint Type')
            DataToDisplay['rsvd2'] = (Frame[2] & 0x0c) >>2
            DataToDisplay['EndIdType'] = Frame[2] & 0x03
            DataToDisplay['EndIdTypeDesc'] = Mctp_Get_Endpoint_Id_Type.get(Frame[2] & 0x03, 'Error Unknown Endpoint ID Type')
            DataToDisplay['MediumSpecific'] = Frame[3]
        #...with invalid payload length
        elif len(Frame[1:]) > 0:
            Template += "{Data[InvalidPayload]} : Error!!! Invalid payload length\n\r"

            DataToDisplay['InvalidPayload'] = [hex(item) for item in Frame[1:]]  #Invalid payload

        #...with no payload
        else:
            Template += "Error!!! No payload\n\r"

    #Unsuccesful response "SUCCESS != Frame[0]:"    
    else:
       #...with unexpected payload
       if len(Frame[1:]) > 0:
           Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"

           DataToDisplay['UnexpectedData'] = [hex(item) for item in Frame[1:]] #Unexpected data
       

    Result = Template.format(Data = DataToDisplay) 
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
    Template = ""

    if len(Frame) == 1:
        Template += "{MsgType:#04x} : {MsgTypeDesc:s}: Message Type Number\n\r"
        Result = Template.format(MsgType = Frame[0],
                                 MsgTypeDesc = GetMctpMessageType(Frame[0]))
    else:
        Result = Template + "Error!!! Invalid length"
    return Result

def ParseMctpGetMctpVersionSupportRes(Frame):
    Template = ""
    DataToDisplay = {}

    #Completion Code
    #Command specific Completion Codes
    MctpGetVersionSupportCompCodes = {0x80 : 'Message type number not supported'}
    #Add common Completion Codes
    MctpGetVersionSupportCompCodes.update(Mctp_Control_Message_Status_Codes)

    Template += "{Data[CompCode]:#04x} : {Data[CompCodeDesc]:s} : Completion Code\n\r"
    DataToDisplay['CompCode']= Frame[0]
    DataToDisplay['CompCodeDesc'] = MctpGetVersionSupportCompCodes.get(Frame[0])
    
    #Successful respone - continue parsing
    if Frame[0] == SUCCESS:
        try:
            Frame_Expected_Length = 2 + (Frame[1]*4)# common data length + entries length
        except:
            Result = Template + "Error!!! Frame length different than expected"
        else:
             if len(Frame) ==  Frame_Expected_Length: 
                Template += "{Data['VersionNumberEntryCount']:#04x} : Version Number Entry count\n\r"
                #<TODO:> Finish implementation

                DataToDisplay['VersionNumberEntryCount']= Frame[1]  #Version Number Entry count
    else:
        if len(Frame) != 1:
            Template += "Error!!! Unexpected Data found"
 
           
            
    Result = Template.format(Data = DataToDisplay) 
    return Result

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
    DataToDisplay = {}

    #Completion Code
    Template += "{Data[CompCode]:#04x} : {Data[CompCodeDesc]:s} : Completion Code \n\r"
    DataToDisplay['CompCode']= Frame[0]
    DataToDisplay['CompCodeDesc'] = Mctp_Control_Message_Status_Codes.get(Frame[0])

    #Successful response 
    if SUCCESS == Frame[0]:
        #calculate payload length
        try:
            PayloadLen = 1 + Frame[1]   # 1 -> magic number stands for MCTP Message Type Count
        except:
            Template += "Error!!! Missing payload Data"
        else:
            #...with valid payload length
            if len(Frame[1:]) == PayloadLen:
                Template += "{Data[MsgTypeCount]:#04x} : MCTP Message Type Count\n\r"

                DataToDisplay['MsgTypeCount']= Frame[1]

                #list supported message types
                for MsgType in Frame[2:]:
                    Template += "{MsgTypeVar:#04x} : {MsgTypeDesc:s} : Message Type Number\n\r".format(MsgTypeVar = MsgType,MsgTypeDesc = GetMctpMessageType(MsgType))

            #...with invalid payload length
            elif len(Frame[1:]) > 0:
                Template += "{Data[InvalidPayload]} : Error!!! Invalid payload length\n\r"

                DataToDisplay['InvalidPayload'] = [hex(item) for item in Frame[1:]]  #Invalid payload

            #...with no payload
            else:
                Template += "Error!!! No payload\n\r"

    #Unsuccesful response "SUCCESS != Frame[0]:"    
    else:
       #...with unexpected payload
       if len(Frame[1:]) > 0:
           Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"

           DataToDisplay['UnexpectedData'] = [hex(item) for item in Frame[1:]] #Unexpected data 
    

    Result = Template.format(Data = DataToDisplay) 
    return Result


#0x06 : 'Get Vendor Defined Message Support',
def ParseMctpGetVendorDefinedMessageSupportReq(Frame):
    Template = ""
    DataToDisplay = {}

    if len(Frame) == 1:
        Template += "{Data[VendorIdSel]:#04x} : Vendor ID Set Selector\n\r"
        DataToDisplay['VendorIdSel'] = Frame[0]
       
    elif len(Frame) > 1:
       Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"
       DataToDisplay['UnexpectedData'] = ([hex(item) for item in Frame[1:]])  #Unexpected data
       
    else :
       Template += "Error!!! Missing data"

    Result = Template.format(Data = DataToDisplay)
    return Result


def ParseMctpGetVendorDefinedMessageSupportRes(Frame):
    Template = ""
    DataToDisplay = {}

    Mctp_Vendor_Id_Sel= {
        0xff : 'No more capability sets'}
   
    Mctp_Vendor_Id_Format = {
        0x00 : {"Name" : "PCI Vendor ID", "Length" : 2},
        0x01 : {"Name" : "IANA Enterprise Number", "Length" : 4}
        }

    #Completion Code
    Template += "{Data[CompCode]:#04x} : {Data[CompCodeDesc]:s} : Completion Code\n\r"
    DataToDisplay['CompCode']= Frame[0]
    DataToDisplay['CompCodeDesc'] = Mctp_Control_Message_Status_Codes.get(Frame[0])

    #Successful respone 
    if SUCCESS == Frame[0]:
        #calculate frame expected length
        Mctp_Frame_Length = len(Frame)

        #paylod should have at least 4 bytes (CC, VendorIdSel, VendorIdFormat, VendorId 1st byte)
        if Mctp_Frame_Length >= 4:
            Mctp_Frame_Expected_Length = 5 + Mctp_Vendor_Id_Format.get(Frame[2],{"Length":0}).get("Length")

            if Mctp_Frame_Expected_Length == Mctp_Frame_Length:
                Template += "{Data[VendorIdSel]:#04x} : {Data[VendorIdSelDesc]:s} : Vendor ID Set Selector\n\r"
                Template += "{Data[VendorIdFormat]:#04x} : {Data[VendorIdFormatDesc]:s} : Vendor Id Format\n\r"
                Template += "{Data[VendorId]} : Vendor ID \n\r"
                Template += "{Data[CmdSetType1]:#04x} {Data[CmdSetType2]:#04x} : Command Set Type\n\r"

                DataToDisplay['VendorIdSel'] = Frame[1]
                DataToDisplay['VendorIdSelDesc'] =  Mctp_Vendor_Id_Sel.get(Frame[1],'Vendor ID Set Selector')
                DataToDisplay['VendorIdFormat'] = Frame[2]
                DataToDisplay['VendorIdFormatDesc'] = (Mctp_Vendor_Id_Format.get(Frame[2],'Error!!! Unknown Vendor ID Format')).get("Name")
                DataToDisplay['VendorId'] = [hex(item) for item in Frame[3:-2]]
                DataToDisplay['CmdSetType1'] = Frame[-2]
                DataToDisplay['CmdSetType2'] = Frame[-1]
                
            else:
                # print faulty data
                Template += "{Data[UnexpectedData]} : Error!!! Frame length different than expected\n\r"
                DataToDisplay['UnexpectedData'] = ([hex(item) for item in Frame[1:]])  #Unexpected data
            
        else:
            # missing data
            Template += "{Data[MissingData]} : Error!!! Missing data\n\r"
            DataToDisplay['MissingData'] = ([hex(item) for item in Frame[1:]])  #Unexpected data
        
    #Unsuccesful respone "SUCCESS != Frame[0]:"
    else:  
        #...with unexpected payload
        if len(Frame[1:]) > 0:
            Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"

            DataToDisplay['UnexpectedData'] = ([hex(item) for item in Frame[1:]])  #Unexpected data
   
            
    Result = Template.format(Data = DataToDisplay) 
    return Result
      

   

#0x07 : 'Resolve Endpoint ID',
def ParseMctpResolveEndpointIdReq(Frame):
    Template = ""

    if len(Frame) == 1:
        Template += "{TargetEndpointId:#04x} : Target Endpoint ID\n\r"
       
        Result = Template.format(TargetEndpointId = Frame[0])
    else:
       Result = Template + "Error!!! Invalid length\n\r"
    return Result


def ParseMctpResolveEndpointIdRes(Frame):
    Template = ""
    DataToDisplay = {}

    #Completion Code
    Template += "{Data[CompCode]:#04x} : {Data[CompCodeDesc]:s} : Completion Code\n\r"
    DataToDisplay['CompCode']= Frame[0]
    DataToDisplay['CompCodeDesc'] = Mctp_Control_Message_Status_Codes.get(Frame[0])
    
    #Successful respone 
    if SUCCESS == Frame[0]:
        #...with valid payload
        if len(Frame[1:]) > 2:
            #(physcial address length - cannot be estimated neither parsed)
            Template += "{Data[BridgeId]:#04x} : Bridge Endpoint ID\n\r"
            Template += "{Data[PhysicalAddress]} : Physical Address\n\r"

            DataToDisplay['BridgeId']=(Frame[1])  #Bridge Endpoint ID
            DataToDisplay['PhysicalAddress']=([hex(item) for item in Frame[2:]]) #Physical Address
        #...with invalid payload
        elif len(Frame[1:]) > 0:
            Template += "{Data[UnexpectedData]} : Error!!! Paylaod too short, missing data\n\r"

            DataToDisplay['UnexpectedData'] = ([hex(item) for item in Frame[1:]])  #Missing data

        #no payload
        else:
            Template += "Error!!! No payload\n\r"


    #Unsuccesful respone "SUCCESS != Frame[0]:"
    else:  
        #...with unexpected payload
        if len(Frame[1:]) > 0:
            Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"

            DataToDisplay['UnexpectedData'] = ([hex(item) for item in Frame[1:]])  #Unexpected data
   
            
    Result = Template.format(Data = DataToDisplay) 
    return Result
       
    

     


#0x08 : 'Allocate Endpoint IDs',
#0x09 : 'Routing Information Update',

#0x0a : 'Get Routing Table Entries',
def ParseMctpGetRoutingTableReq(Frame):
    Template = ""
    DataToDisplay = {}

    if len(Frame) == 1:
        Template += "{Data[EntryHandle]:#04x} : Entry Handle\n\r"
        DataToDisplay['EntryHandle'] = Frame[0]
       
    elif len(Frame) > 1:
       Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"
       DataToDisplay['UnexpectedData'] = ([hex(item) for item in Frame[1:]])  #Unexpected data
       
    else :
       Template += "Error!!! Missing data"

    Result = Template.format(Data = DataToDisplay)
    return Result


def GetEntryLength(Frame):
    #Each entry contains 6 bytes of common data + medium-specific physical address,
    #medium-specific physical address length is in byte 6th byte 
    try:
        EntryLength =  6 + Frame[5]
        return EntryLength
    except:
        return 0
    
def ParsePciePhysicalAddress(Address):
    Template = ""
    Template += str(["{Item:#04x}".format(Item = ii) for ii in Address]) + " : PCIe Address \n\r"
    Template += "\t{Bus:#04x} : Bus, \n\r"
    Template += "\t{Dev:#04x} : Device, \n\r"
    Template += "\t{Func:#04x} : Function.\n\r"

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
    Template = ""
    DataToDisplay = {}
    
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
    Template += "{Data[SizeEidRange]:#04x} : Size of EID range associated with this entry\n\r"
    Template += "{Data[StartingEid]:#04x} : Starting EID\n\r"
    Template += "{Data[Byte3]:#04x} : Entry Type/Port Number:\n\r"
    Template += "\t{Data[EntryType]:#02b} : {Data[EntryTypeDesc]:s} : Entry Type,\n\r"
    Template += "\t{Data[DynStatEntry]:#01b} : {Data[DynStatEntryDesc]:s} : Dynamic/Static Entry,\n\r"
    Template += "\t{Data[PortNumber]:#04x} : Port Number.\n\r"
    Template += "{Data[PhyTransBinding]:#04x} : {Data[PhyTransBindingDesc]:s} : Physical Transport Binding\n\r"
    Template += "{Data[PhyMediaId]:#04x} : {Data[PhyMediaIdDesc]:s} : Physical Medium \n\r"
    Template += "{Data[PhyAddrSize]:#04x} : Physical Address Size\n\r"
    Template += ParsePhysicalAddress(Entry[3],Entry[6:])

    DataToDisplay['SizeEidRange'] = Entry[0]
    DataToDisplay['StartingEid'] = Entry[1]
    DataToDisplay['Byte3'] = Entry[2]
    DataToDisplay['EntryType'] = (Entry[2] & 0xc0) >> 6
    DataToDisplay['EntryTypeDesc'] = Mctp_Entry_Type.get((Entry[2] & 0xc0) >> 6, 'Error!!! Unknown Entry Type')
    DataToDisplay['DynStatEntry'] = (Entry[2] & 0x20) >> 5
    DataToDisplay['DynStatEntryDesc'] = Mctp_DynStat_Entry.get((Entry[2] & 0x20) >> 5,'Error!!! Unknown Dynamic or Static Type')
    DataToDisplay['PortNumber'] = (Entry[2] & 0x1f)
    DataToDisplay['PhyTransBinding'] = Entry[3]
    DataToDisplay['PhyTransBindingDesc'] = Mctp_Physical_Transport_Bindings.get(Entry[3],'Reserved')
    DataToDisplay['PhyMediaId'] = Entry[4]
    DataToDisplay['PhyMediaIdDesc'] = Mctp_Physical_Medium_Identifiers.get(Entry[4],'Reserved')
    DataToDisplay['PhyAddrSize'] = Entry[5]
    
    Result = Template.format(Data = DataToDisplay)
    return Result
   
def ParseMctpGetRoutingTableRes(Frame):
    Template = ""
    DataToDisplay = {}

    Mctp_Entry_Handle= {
        0xff : 'No more entries'}
   
    Mctp_Frame_Length = len(Frame)
    Mctp_Frame_Expected_Length = 0

    #Completion Code
    Template += "{Data[CompCode]:#04x} : {Data[CompCodeDesc]:s} : Completion Code \n\r"
    DataToDisplay['CompCode']= Frame[0]
    DataToDisplay['CompCodeDesc'] = Mctp_Control_Message_Status_Codes.get(Frame[0])
   
    #The Frame with SUCCESS CC shall have at minimum 3 bytes (3 common data bytes)
    if SUCCESS == Frame[0]:
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

                Template += "{Data[NextEntry]:#04x} : {Data[NextEntryDesc]:s} : Next Entry Handle\n\r"
                Template += "{Data[EntriesCount]:#04x} : Entries Count in this response\n\r"
                
                DataToDisplay['NextEntry'] = Frame[1] #Next Entry Handle
                DataToDisplay['NextEntryDesc'] = Mctp_Entry_Handle.get(Frame[1],'Next Entry Handle') #Next Entry Handle Description
                DataToDisplay['EntriesCount']= Frame[2] #Entries Count
                
                for Entry in GetRoutingTableEntries:
                    Template += ParseGetRoutingEntry(Entry)

            else:
                # print faulty data
                Template += "{Data[UnexpectedData]} : Error!!! Frame length different than expected\n\r"
                DataToDisplay['UnexpectedData'] = ([hex(item) for item in Frame[1:]])  #Unexpected data
                
        else:
            # missing data
            Template += "{Data[UnexpectedData]} : Error!!! Missing data\n\r"
            DataToDisplay['UnexpectedData'] = ([hex(item) for item in Frame[1:]])  #Unexpected data


    #The Frame with other CC shall have at minimum 1 byte
    else:
        if Mctp_Frame_Length > 1:
            #Unexpected data
            Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"
            DataToDisplay['UnexpectedData'] = ([hex(item) for item in Frame[1:]])  #Unexpected data                                 
   
    Result = Template.format(Data = DataToDisplay) 
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
    DataToDisplay = {}

    #Completion Code
    Template += "{Data[CompCode]:#04x} : {Data[CompCodeDesc]:s} : Completion Code\n\r"
    DataToDisplay['CompCode']= Frame[0]
    DataToDisplay['CompCodeDesc'] = Mctp_Control_Message_Status_Codes.get(Frame[0])

    #Unexpected payload
    if len(Frame[1:]) > 0:
        Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"
        DataToDisplay['UnexpectedData'] = [hex(item) for item in Frame[1:]] #Unexpected data

    Result = Template.format(Data = DataToDisplay) 
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
    DataToDisplay = {}

    #Completion Code
    Template += "{Data[CompCode]:#04x} : {Data[CompCodeDesc]:s} : Completion Code\n\r"
    DataToDisplay['CompCode']= Frame[0]
    DataToDisplay['CompCodeDesc'] = Mctp_Control_Message_Status_Codes.get(Frame[0])

    #Unexpected payload
    if len(Frame[1:]) > 0:
        Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"
        DataToDisplay['UnexpectedData'] = [hex(item) for item in Frame[1:]] #Unexpected data

    Result = Template.format(Data = DataToDisplay) 
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
    DataToDisplay = {}

    #Completion Code
    Template += "{Data[CompCode]:#04x} : {Data[CompCodeDesc]:s} : Completion Code\n\r"
    DataToDisplay['CompCode']= Frame[0]
    DataToDisplay['CompCodeDesc'] = Mctp_Control_Message_Status_Codes.get(Frame[0])

    #Unexpected payload
    if len(Frame[1:]) > 0:
        Template += "{Data[UnexpectedData]} : Error!!! Unexpected data\n\r"
        DataToDisplay['UnexpectedData'] = [hex(item) for item in Frame[1:]] #Unexpected data

    Result = Template.format(Data = DataToDisplay) 
    return Result

#0x0e : 'Get Network ID',
def ParseMctpGetNetworkIdReq(Frame):
    ...
    return ""
   
def ParseMctpGetNetworkIdRes(Frame):
    ...
    return ""


#0x0f : 'Query Hop'


Mctp_Control_Message_Handlers = {
    0x00 : {'Req' : None, 'Res': None}, #Reserved
    0x01 : {'Req' : ParseMctpSetEndpointEidReq, 'Res': ParseMctpSetEndpointEidRes}, #Done + Fixed + Unified
    0x02 : {'Req' : ParseMctpGetEndpointEidReq, 'Res': ParseMctpGetEndpointEidRes}, #Done + Fixed + Unified
    0x03 : {'Req' : ParseMctpGetEndpointUuidReq, 'Res': ParseMctpGetEndpointUuidRes},
    0x04 : {'Req' : ParseMctpGetMctpVersionSupportReq, 'Res': ParseMctpGetMctpVersionSupportRes},
    0x05 : {'Req' : ParseMctpGetMessageTypeSupportReq, 'Res': ParseMctpGetMessageTypeSupportRes}, #Done + Fixed + Unified
    0x06 : {'Req' : ParseMctpGetVendorDefinedMessageSupportReq, 'Res': ParseMctpGetVendorDefinedMessageSupportRes}, #Done + Fixed + Unified
    0x07 : {'Req' : ParseMctpResolveEndpointIdReq, 'Res': ParseMctpResolveEndpointIdRes}, #Done + Fixed + Unified
    0x08 : {'Req' : None, 'Res': None},
    0x09 : {'Req' : None, 'Res': None},
    0x0a : {'Req' : ParseMctpGetRoutingTableReq, 'Res': ParseMctpGetRoutingTableRes}, #Done + Fixed + Unified
    0x0b : {'Req' : ParseMctpPrepareForEndpointDiscoveryReq, 'Res': ParseMctpPrepareForEndpointDiscoveryRes}, #Done + Fixed + Unified
    0x0c : {'Req' : ParseMctpEndpointDiscoveryReq, 'Res': ParseMctpEndpointDiscoveryRes}, #Done + Fixed + Unified
    0x0d : {'Req' : ParseMctpDiscoveryNotifyReq, 'Res': ParseMctpDiscoveryNotifyRes}, #Done + Fixed + Unified
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

def GetRqDesc(Rq):
    Mctp_Rq_Bit= {
            0b00 : 'Response',
            0b01 : 'Request',
            }
    return Mctp_Rq_Bit.get(Rq,"Error!!! Illegal value")

def ParseMctpControlFrameCommonHeader(Frame):
    Template =  "\n\r"
    Template += "{FirstByte:#04x} : \n\r"
    Template += "\t{IC:#03b} : IC, \n\r"
    Template += "\t0x00 : MCTP Control Command : Message Type.\n\r"
    Template += "{SecondByte:#04x} :\n\r"
    Template += "\t{Rq:#03b} : {RqDesc:s} : Request Bit,\n\r"
    Template += "\t{D:#03b} : Datagram Bit,\n\r"
    Template += "\t{rsvd:#03b} : Reserved,\n\r"
    Template += "\t{InsID:#d} : Instance ID. \n\r"
    Template += "{CommandCode:#04x} : {CommandDesc:s} : Command Code\n\r"

    Result = Template.format(FirstByte = Frame[0],
                             IC = (Frame[0] & 0x80) >>7,
                             SecondByte = Frame[1],
                             Rq = (Frame[1] & 0x80) >>7,
                             RqDesc = GetRqDesc((Frame[1] & 0x80) >>7),
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

        #Before looking for parsing function, validate payload existance
        #Response payload shall contain at least Completion Code
        #Request payload can be empty
        if not RqBit and not Frame[3:]:
            Template += "Error!!! Missing response Completion Code and payload\n\r" 
        else:    
            #Get Parsing Function
            MctpControlFramePayloadParser = GetMctpControlFramePayloadParser(RqBit,Frame[2])
            if None != MctpControlFramePayloadParser:
                Template += MctpControlFramePayloadParser(Frame[3:])
            else:
                Template += "\n\r No parser found\n\r"

        Result = Template.format()
    else:
        Result = Template + "Error!!! Invalid data length\n\r"

    #Output parsed MCTP Control frame
    return Result

def ParseMctpVendorDefinedPcieFrame(Packet_Data):
    Result = "VDM Frame"
    ...
    return Result

#<TODO> Use dictornary!!!
def ParseMctpPacketPayload(Packet_Data):
    Msg_Type = Packet_Data[0] & 0x7f

    #<TODO:> Replace magic numbers with const!!!
    if 0x00 == Msg_Type:
        Result = ParseMctpControlFrame(Packet_Data)
    elif 0x7e == Msg_Type:
        Result = ParseMctpVendorDefinedPcieFrame(Packet_Data)
    else:
        Result = "Parser unsupported message type"
    return Result


def ParseMctpTransportHeader(Header):
    Template = "MCTP Transport Header:"
    if len(Header) == 4:
        Template += "\n\r"
        Template += "{FirstByte:#04x} : \n\r"
        Template += "\t{Rsvd:#x} : Reserved, \n\r"
        Template += "\t{HeadVer:#x} : Header Version.\n\r"
        Template += "{DestEid:#04x} : {DestEidDesc:s} : Destination endpoint ID\n\r"
        Template += "{SrcEid:#04x} : {SrcEidDesc:s} : Source endpoint ID\n\r"
        Template += "{ForthByte:#04x} : \n\r" 
        Template += "\t{SOM:#03b} : SOM,\n\r"
        Template += "\t{EOM:#03b} : EOM, \n\r"
        Template += "\t{PktSeq:#d} : PktSeq#, \n\r"
        Template += "\t{TO:#03b} : Tag Owner, \n\r"
        Template += "\t{MsgTag:#d} : Message Tag."
       
        Result = Template.format(FirstByte = Header[0],
                        Rsvd= Header[0]>>4,
                        HeadVer = Header[0] & 0x0f,
                        DestEid = Header[1],
                        DestEidDesc = GetMctpDestEidDesc(Header[1]),
                        SrcEid = Header[2],
                        SrcEidDesc = GetMctpSrcEidDesc(Header[2]),
                        ForthByte = Header[3],
                        SOM = (Header[3] & 0x80)>>7,
                        EOM = (Header[3] & 0x40)>>6,
                        PktSeq = (Header[3] & 0x30)>>4,
                        TO = (Header[3] & 0x8)>>3,
                        MsgTag = (Header[3] & 0x7))
      
    else:
        Result =Template + "Error Invalid length"
       
    return Result


def ParseMctpFrame(Frame):
    if len(Frame) >= 5:
        Result = ParseMctpTransportHeader(Frame[:4])
        Result += ParseMctpPacketPayload(Frame[4:])
    else:
        Result = "Invalid MCTP Frame length"
    return Result

#----Script Start----
if __name__ == "__main__":

#--------------------------------------------------Start 0x01------------------------------------------------------------------------------------------------------
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x01, 0x00, 0x60]    #Set EID Req
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x01, 0x00, 0x00, 0x60, 0x03]    #Set EID Res, succesfull, valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x01, 0x00, 0x00, 0x60]    #Set EID Res, succesfull, invalid - too short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x01, 0x00, 0x00, 0x60, 0x61, 0x62]    #Set EID Res, succesfull, invalid - too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x01, 0x00]    #Set EID Res, succesfull, invalid - no payload
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x01, 0x04]    #Set EID Res, Unsuccesfull, valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x01, 0x02, 0x11, 0x22]    #Set EID Res, Unsuccesfull, invalid - unexpected payload
    ParseMctpFrame(Mctp_Test_Frame)

#--------------------------------------------------End 0x01--------------------------------------------------------------------------------------------------------
#--------------------------------------------------Start 0x02------------------------------------------------------------------------------------------------------

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x02]    #Get EID Req
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x02, 0x00, 0x61, 0x00, 0x00]    #Get EID Res, successful, valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x02, 0x00, 0x61, 0x00]    #Get EID Res, successful, invalid - too short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x02, 0x00, 0x61, 0x00, 0x22, 0x33]    #Get EID Res, successful, invalid - too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x02, 0x00]    #Get EID Res, successful, invalid - no payload
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x02, 0x01]    #Get EID Res, unsuccessful, valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x02, 0x01, 0x99]    #Get EID Res, unsuccessful, invalid - unexpected payload
    ParseMctpFrame(Mctp_Test_Frame)

#--------------------------------------------------End 0x02--------------------------------------------------------------------------------------------------------

#--------------------------------------------------Start 0x05------------------------------------------------------------------------------------------------------
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x05]    #Get Message Type Support Req, valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x05, 0x77]    #Get Message Type Support Req, invalid - too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x05, 0x00, 0x02, 0x00, 0x7e ]    #Get Message Type Support Res, successful, valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x05, 0x00, 0x02, 0x00, 0x7e, 0x66 ]    #Get Message Type Support Res, successful, invalid - too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x05, 0x00, 0x02, 0x00 ]    #Get Message Type Support Res, successful, invalid - too short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x05, 0x00 ]    #Get Message Type Support Res, successful, invalid - no payload
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x05, 0x04 ]    #Get Message Type Support Res, unsuccessful, valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x05, 0x04, 0x99 ]    #Get Message Type Support Res, unsuccessful, invalid - unexpected payload
    ParseMctpFrame(Mctp_Test_Frame)
#--------------------------------------------------End 0x05--------------------------------------------------------------------------------------------------------

#--------------------------------------------------Start 0x07------------------------------------------------------------------------------------------------------
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x07, 0x50]    #Request, valid 
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x07]    #Request, wrong length, missing data 
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x07, 0x50, 0x51]    #Request, wrong length, too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x07, 0x00, 0x50, 0x12, 0x34]    #Response, successfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)
    
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x07, 0x00, 0x50]    #Response, successfull ,invalid - too short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x07, 0x00]    #Response, successfull ,invalid - no payload
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x07]    #Response, successfull , no CC + no payload 
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x07, 0x03]    #Response, unsuccessfull ,valid 
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x31, 0x32, 0xD9, 0x00, 0x07, 0x07, 0x03, 0x99, 0x88]    #Response, unsuccessfull ,invalid 
    ParseMctpFrame(Mctp_Test_Frame)
#--------------------------------------------------End 0x07------------------------------------------------------------------------------------------------------

#--------------------------------------------------Start 0x0b------------------------------------------------------------------------------------------------------
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x0b]    #Request, valid 
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x0b, 0x99, 0x88]    #Request, invalid, unexpected data
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0b, 0x00]    #Response, successfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0b, 0x00, 0x99, 0x88]    #Response, successfull ,invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0b, 0x01]    #Response, unsuccessfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0b, 0x02, 0x99, 0x88]    #Response, unsuccessfull ,invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)
#--------------------------------------------------End 0x0b------------------------------------------------------------------------------------------------------
    
#--------------------------------------------------Start 0x0c------------------------------------------------------------------------------------------------------
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x0c]    #Request, valid 
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x0c, 0x99, 0x88]    #Request, invalid, unexpected data
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0c, 0x00]    #Response, successfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0c, 0x00, 0x99, 0x88]    #Response, successfull ,invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0c, 0x01]    #Response, unsuccessfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0c, 0x02, 0x99, 0x88]    #Response, unsuccessfull ,invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)
#--------------------------------------------------End 0x0c------------------------------------------------------------------------------------------------------

#--------------------------------------------------Start 0x0d----------------------------------------------------------------------------------------------------
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x0d]    #Request, valid 
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x0d, 0x99, 0x88]    #Request, invalid, unexpected data
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0d, 0x00]    #Response, successfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0d, 0x00, 0x99, 0x88]    #Response, successfull ,invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0d, 0x01]    #Response, unsuccessfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0d, 0x02, 0x99, 0x88]    #Response, unsuccessfull ,invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)
#--------------------------------------------------End 0x0d------------------------------------------------------------------------------------------------------

#--------------------------------------------------Start 0x0a----------------------------------------------------------------------------------------------------
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x0a, 0x02]    #Request, valid 
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x0a, 0x02, 0x99, 0x88]    #Request, invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x0a]    #Request, invalid, too short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x02]    #Response, unsuccessfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x02, 0x99, 0x88]    #Response, unsuccessfull ,invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x00]    #Response, successfull ,invalid, too short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x00, 0xff, 0x01, 0x01, 0x50,0x20, 0x02, 0x0a, 0x02, 0x00, 0x92]    #Response, successfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x00, 0xff, 0x02, 0x01, 0x50,0x20, 0x02, 0x0a, 0x02, 0x00, 0x92, 0x01, 0x51,0x20, 0x02, 0x0a, 0x02, 0x00, 0x93]    #Response, successfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x00, 0xff, 0x01, 0x01, 0x50,0x20, 0x02, 0x0a, 0x02, 0x00, 0x92, 0x01, 0x51,0x20, 0x02, 0x0a, 0x02, 0x00, 0x93]    #Response, successfull ,invalid, longer than expected
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x00, 0xff, 0x02, 0x01, 0x50,0x20, 0x02, 0x0a, 0x02, 0x00, 0x92, 0x01, 0x51, 0x02, 0x0a, 0x02, 0x00, 0x93]    #Response, successfull ,invalid, shorter than expected
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x00]    #Response, successfull ,invalid, missing payload
    ParseMctpFrame(Mctp_Test_Frame)
    
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x00, 0x99]    #Response, successfull ,invalid, payload to short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x00, 0x99, 0x88, 0x77]    #Response, successfull ,invalid, payload to short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x0a, 0x00, 0x99, 0x88, 0x77, 0x66]    #Response, successfull ,invalid, payload to short
    ParseMctpFrame(Mctp_Test_Frame)

#--------------------------------------------------End 0x0a------------------------------------------------------------------------------------------------------

#--------------------------------------------------Start 0x06----------------------------------------------------------------------------------------------------
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x06, 0x02]    #Request, valid 
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x06, 0x02, 0x99, 0x88]    #Request, invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x06]    #Request, invalid, too short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x06, 0x02]    #Response, unsuccessfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x06, 0x02, 0x99, 0x88]    #Response, unsuccessfull ,invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x06, 0x00]    #Response, successfull ,invalid, too short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x06, 0x00, 0x99]    #Response, successfull ,invalid, too short
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x06, 0x00, 0xff, 0x02, 0x99]    #Response, successfull ,invalid, unknown vendor format
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x06, 0x00, 0xff, 0x00, 0x80, 0x86, 0x00, 0x01]    #Response, successfull ,valid
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x06, 0x00, 0xff, 0x00, 0x80, 0x86, 0x00, 0x01, 0x99]    #Response, successfull ,invalid, too long
    ParseMctpFrame(Mctp_Test_Frame)

    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x07, 0x06, 0x00, 0xff, 0x00, 0x80, 0x86, 0x00]    #Response, successfull ,invalid, too short
    ParsedFrame = ParseMctpFrame(Mctp_Test_Frame)
    print(ParsedFrame)
#--------------------------------------------------End 0x07------------------------------------------------------------------------------------------------------
