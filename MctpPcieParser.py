# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 20:06:18 2017

@author: M
"""

#MCTP PCIe VDM frame parser

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
    #parse PCIe VDM Header
    #parse PCIe VDM Data (parse MCTP Frame)
    return

#----Script Start----
if __name__ == "__main__":

    RoutingTst = 0b000
    print(GetMctpPcieVdmRoutingType(RoutingTst))
    
    RoutingTst = 0b010
    print(GetMctpPcieVdmRoutingType(RoutingTst))
    
    RoutingTst = 0b011
    print(GetMctpPcieVdmRoutingType(RoutingTst))
    
    RoutingTst = 0b111
    print(GetMctpPcieVdmRoutingType(RoutingTst))