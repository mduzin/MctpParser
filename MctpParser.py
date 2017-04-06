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
     


#0x01 : 'Set Endpoint EID'
def ParseMctpSetEndpointEidReq(Frame):
    ...
    return ""
def ParseMctpSetEndpointEidRes(Frame):
    ...
    return ""
#0x02 : 'Get Endpoint EID'
def ParseMctpGetEndpointEidReq(Frame):
    ...
    return ""
def ParseMctpGetEndpointEidRes(Frame):
    ...
    return ""
        
    
#0x03 : 'Get Endpoint UUID'
def ParseMctpGetEndpointUuidReq(Frame):
    ...
    return ""
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


Mctp_Control_Message_Handlers = {
    0x00 : {'Req' : None, 'Res': None},
    0x01 : {'Req' : ParseMctpSetEndpointEidReq, 'Res': ParseMctpSetEndpointEidRes},
    0x02 : {'Req' : ParseMctpGetEndpointEidReq, 'Res': ParseMctpGetEndpointEidRes},
    0x03 : {'Req' : ParseMctpGetEndpointUuidReq, 'Res': ParseMctpGetEndpointUuidRes},
    0x04 : {'Req' : ParseMctpGetMctpVersionSupportReq, 'Res': ParseMctpGetMctpVersionSupportRes},
    0x05 : {'Req' : None, 'Res': None},
    0x06 : {'Req' : None, 'Res': None},
    0x07 : {'Req' : None, 'Res': None},
    0x08 : {'Req' : None, 'Res': None},
    0x09 : {'Req' : None, 'Res': None},
    0x0a : {'Req' : None, 'Res': None},
    0x0b : {'Req' : None, 'Res': None},
    0x0c : {'Req' : None, 'Res': None},
    0x0d : {'Req' : None, 'Res': None},
    0x0e : {'Req' : None, 'Res': None},
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
    Template += "{FirstByte:#04x} : {IC:x} : IC, 0x00 : MCTP Control Command,\n\r" 
    Template += "{SecondByte:#04x} : {Rq:x} : Rq, {D:x} : D, {rsvd:x} : rsvd, {InsID:x} : Instance ID \n\r"
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
            Template =  "\n\r"
            Template + "No handle found"

        Result = Template.format()
    else:
        Result = Template + "Error Invalid length"

    print(Result)
    return Result


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
    Mctp_Test_Frame = [0x01, 0x00, 0x00, 0xD9, 0x00, 0x87, 0x02]
    Mctp_Test_Transport_Header = Mctp_Test_Frame[:4]
    #print(MctpTestTransportHeader)
    #print(ParseMctpTransportHeader(MctpTestTransportHeader))

    ParseMctpFrame(Mctp_Test_Frame)
    
    #print(GetMctpControlMessageCommandCode(0x00))
    #print(GetMctpControlMessageCommandCode(0x01))
    #print(GetMctpControlMessageCommandCode(0x02))
    #print(GetMctpControlMessageCommandCode(0x1f))
    #print("")
    #print(ParseMctpTransportHeader([0x11,0x12,0x13]))
    #print(ParseMctpTransportHeader([0xf1,0x11,0x12,0x13]))
    #print("")
    #print(ParseMctpControlFrame([0xf1,0x11,0x02,0x00]))
