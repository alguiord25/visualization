#!/usr/bin/env python3

##Raspberry Pi receiver

from RF24 import *
from datetime import datetime,timedelta
#import spidev
import csv

radio = RF24(25, 0);

pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]

print('Executin rpi_receiver')
radio.begin()
radio.enableDynamicPayloads()
radio.setChannel(0x4C)
radio.setRetries(5,15)
radio.setDataRate(RF24_250KBPS)
radio.printDetails()

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1,pipes[0])
radio.startListening()

def writeSensor(sensor, data):
    myfile ="%s.csv" % sensor
    with open(myfile, 'a+', newline='') as csvfile:
         datawriter = csv.writer(csvfile, delimiter=',',
                      quotechar='|', quoting=csv.QUOTE_MINIMAL)
         now = datetime.now()
         now = now.strftime("%y-%m-%d %H:%M")
         datawriter.writerow([now, data])


def parseRow(row):
    rowcontent = row.split("!")[0]
    rowsplited = rowcontent.split(" ")
    sensor = rowsplited[0]
    rowsplited = rowsplited[1:] 
    for mycol in rowsplited:
      print(mycol)
      sensordata = mycol.split(":")
      sensorItem = "%s_%s" % (sensor,sensordata[0])
      writeSensor(sensorItem, int(sensordata[1])) 


while(1):    
    if radio.available():    
        len = radio.getDynamicPayloadSize()
        receive_payload = radio.read(len)
        a = receive_payload.decode('ascii')
        a = a.replace("\x00\x00","")
        print(a)
        parseRow(a)
	
