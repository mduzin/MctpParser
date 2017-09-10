# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 20:06:18 2017
@author: M
"""

import sys
import MctpPcieParser


def MctpLineParse(RawData):
   if RawData:
      MctpPcieFrame = [int('0x'+item, 16) for item in RawData.split()]
      MctpPcieParser.ParseMctpPcieFrame(MctpPcieFrame)
   return

#----Script Start----
if __name__ == "__main__":
   #input file from cmd line
   try:
      LogFileName = sys.argv[1]
   except:
      print("Error!!!: No input file.")
   else:
      #read and parse log line 
      for line in open(LogFileName):
         print("Parsed Frame: " + line.upper())
         MctpLineParse(line)
   
