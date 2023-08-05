##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
### Steps  : 
###
##########################################################
### User Entry
##########################################################
import os
BaseDir = os.path.dirname(os.path.realpath(__file__))
OutFile = BaseDir + "\\" + __file__

FSW_IP  = '192.168.1.109'
FsArry  = [100e6, 115.2e6, 200e6, 400e6, 800e6, 1200e6, 1600e6, 2000e6] #Sampling Rate
MeasTim = 500e-6

##########################################################
### Code Overhead
##########################################################
from     rssd.FSW_Common   import VSA
from     datetime          import datetime
import   rssd.FileIO

f = rssd.FileIO.FileIO()
OFile = f.Init(OutFile)
FSW = VSA()                         #Create FSW Object
FSW.jav_Open(FSW_IP,f.sFName)       #Connect to FSW
if 0:
   FSW.jav_logSCPI()
   
FSW.jav_Reset()
FSW.Init_IQ()                       #FSW IQ Channel
FSW.Set_DisplayUpdate("OFF")
FSW.Set_SweepTime(MeasTim)
FSW.Set_SweepCont(0)

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Fs,CapTime,Iter,CmdTime')
for Fs in FsArry:
   print("Starting Fs: %f"%Fs)
   FSW.Set_IQ_SamplingRate(Fs)
   for i in range(50):
      tick = datetime.now()
      FSW.Set_InitImm()
      FSW.Get_IQ_Data()
      d = datetime.now() - tick
      OutStr = '%f,%f,%d,%3d.%06d'%(Fs/1e6,MeasTim,i,d.seconds,d.microseconds)
      OFile.write (OutStr)
   
##########################################################
### Cleanup Automation
##########################################################
FSW.jav_Close()
OFile.close()
