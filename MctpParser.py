# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 20:32:19 2017

@author: M
"""

#MCTP frame parser

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

#MCTP transport header parser function
def ParseMctpTransportHeader(Header):
    Template = "MCTP Transport Header: "
    if len(Header) == 4:
        Template += "\n\r"
        Template += "{FirstByte:#04x} : {Rsvd:x} : Reserved, {Head_Ver:x} : Header Version,\n\r" 
        Template += "{Dest_Eid:#04x} : Destination endpoint ID,\n\r"
        Template += "{Src_Eid:#04x} : Source endpoint ID,\n\r"
        Template += "{ForthByte:#04x} : {SOM:x} : SOM, {EOM:x} : EOM, {PktSeq:x} : PktSeq#, {TO:x} : TO, {MsgTag:x} : MsgTag"
        
        Template = Template.format(FirstByte = Header[0],
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
        Template += "Error Invalid length"
        
    return Template
        
def GetMctpControlMessageCommandCode(CmdCode):
    return '{Code:#04x} : {Desc}'.format(Code = CmdCode, Desc = Mctp_Control_Message_Command_Codes.get(CmdCode,'Transport Specific Command Code'))

    


def ParseMctpControlFrame(FrameData):
    ...

def ParseMctpSetEndpointEidReq():
    ...
def ParseMctpSetEndpointEidRes():
    ...

def ParseMctpGetEndpointEidReq():
    ...
def ParseMctpGetEndpointEidRes():
    ...



#----Script Start----
if __name__ == "__main__":
    
    
    print(GetMctpControlMessageCommandCode(0x00))
    print(GetMctpControlMessageCommandCode(0x01))
    print(GetMctpControlMessageCommandCode(0x02))
    print(GetMctpControlMessageCommandCode(0x1f))
    print("")
    print(ParseMctpTransportHeader([0x11,0x12,0x13]))
    print(ParseMctpTransportHeader([0xf1,0x11,0x12,0x13]))
