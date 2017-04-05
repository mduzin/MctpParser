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
    0x05 : 'ERROR_UNSUPPORTED_CMD'
    }

def GetMctpControlMessageCommandCode(CmdCode):
    return '{Code:#04x} : {Desc}'.format(Code = CmdCode, Desc = Mctp_Control_Message_Command_Codes.get(CmdCode,'Transport Specific Command Code'))
    
def GetMctpControlMessageCommandName(CmdCode):
    return Mctp_Control_Message_Command_Codes.get(CmdCode,'Reserved')
    
def GetMctpMessageType(TypeCode):
    return Mctp_Message_Types.get(TypeCode,'Reserved')
    
#MCTP transport header parser function
def ParseMctpTransportHeader(Header):
    Template = "MCTP Transport Header: "
    if len(Header) == 4:
        Template += "\n\r"
        Template += "{FirstByte:#04x} : {Rsvd:x} : Reserved, {Head_Ver:x} : Header Version,\n\r" 
        Template += "{Dest_Eid:#04x} : Destination endpoint ID,\n\r"
        Template += "{Src_Eid:#04x} : Source endpoint ID,\n\r"
        Template += "{ForthByte:#04x} : {SOM:x} : SOM, {EOM:x} : EOM, {PktSeq:x} : PktSeq#, {TO:x} : TO, {MsgTag:x} : MsgTag"
        
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
        
    return Result
    
def GetMctpControlFramePayload(RqBit,CommandCode):
    ...
    return ""

def ParseMctpControlFrame(Frame):
    Template = "MCTP Control Frame: "
    if len(Frame) >= 3:
        #<TODO:> check if 
        Template += "\n\r"
        Template += "{FirstByte:#04x} : {IC:x} : IC, 0x00 : MCTP Control Command,\n\r" 
        Template += "{SecondByte:#04x} : {Rq:x} : Rq, {D:x} : D, {rsvd:x} : rsvd, {InsID:x} : Instance ID \n\r"
        Template += "{CommandCode:#04x} : {CommandDesc:s} \n\r"
        
        RqBit = (Frame[1] & 0x80) >>7

        Template += GetMctpControlFramePayload(RqBit,Frame[2])
        
        Result = Template.format(FirstByte = Frame[0],
                                 IC = (Frame[0] & 0x80) >>7,
                                 SecondByte = Frame[1],
                                 Rq = RqBit,
                                 D = (Frame[1] & 0x40) >> 6,
                                 rsvd = (Frame[1] & 0x20) >> 5,
                                 InsID = (Frame[1] & 0x1f),
                                 CommandCode = Frame[2],
                                 CommandDesc = GetMctpControlMessageCommandName(Frame[2]))
    else:
        Result =Template + "Error Invalid length"
    return Result
    
def ParseMctpPacketPaylod(FrameData):

    MsgType = FrameData[0] & 0x7f
    if 0x00 == MsgType:
        ParseMctpControlFrame(FrameData)

    return
    

 



#0x01 : 'Set Endpoint EID'
def ParseMctpSetEndpointEidReq():
    ...
def ParseMctpSetEndpointEidRes():
    ...
    
#0x02 : 'Get Endpoint EID'
def ParseMctpGetEndpointEidReq():
    ...
def ParseMctpGetEndpointEidRes():
    ...
    
#0x03 : 'Get Endpoint UUID'
def ParseMctpGetEndpointUuidReq():
    ...
def ParseMctpGetEndpointUuidRes():
    ...
        
#0x04 : 'Get MCTP Version Support',
def ParseMctpGetMctpVersionSupportReq():
    ...
def ParseMctpGetMctpVersionSupportRes():
    ...

#0x05 : 'Get Message Type Support',
#0x06 : 'Get Vendor Defined Message Support',
#0x07 : 'Resolve Endpoint ID',
#0x08 : 'Allocate Endpoint IDs',
#0x09 : 'Routing Information Update',
#0x0a : 'Get Routing Table Entries',
#0x0b : 'Prepare for Endpoint Discovery',
#0x0c : 'Endpoint Discovery',
#0x0d : 'Discovery Notify',
#0x0e : 'Get Network ID',
#0x0f : 'Query Hop'}


#----Script Start----
if __name__ == "__main__":
    
    
    print(GetMctpControlMessageCommandCode(0x00))
    print(GetMctpControlMessageCommandCode(0x01))
    print(GetMctpControlMessageCommandCode(0x02))
    print(GetMctpControlMessageCommandCode(0x1f))
    print("")
    print(ParseMctpTransportHeader([0x11,0x12,0x13]))
    print(ParseMctpTransportHeader([0xf1,0x11,0x12,0x13]))
    print("")
    print(ParseMctpControlFrame([0xf1,0x11,0x02,0x00]))
