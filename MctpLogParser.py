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
      Result = MctpPcieParser.ParseMctpPcieFrame(MctpPcieFrame)
   else:
      Result = "Error!!!: No Data"
   return Result

#----Script Start----
if __name__ == "__main__":
   #input file from cmd line
   try:
      LogFileName = sys.argv[1]
   except:
      print("Error!!!: No input file.")
   else:
      #read and parse log line
      fh = open("ParsedLog.txt","w")
      for line in open(LogFileName):
         print("Parsed Frame: " + line.upper(),file = fh)
         print(MctpLineParse(line),file = fh)
      fh.close()
   
