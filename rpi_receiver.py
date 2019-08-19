#!/usr/bin/env python3

##Raspberry Pi receiver

from RF24 import *
from datetime import datetime,timedelta
from timeit import default_timer as timer
import RPi.GPIO as GPIO
#import spidev
import csv
import os

radio = RF24(25, 0);

pipes = [0xF1F0F0F0E0, 0xF0F0F0F0D2]

print('Executin rpi_receiver')
radio.begin()
radio.enableDynamicPayloads()
radio.setAutoAck(True)
radio.setChannel(0x4C)
radio.setRetries(50,15)
radio.setDataRate(RF24_250KBPS)
radio.printDetails()

#radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1,pipes[0])
radio.startListening()


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, False)
start = timer();
end = timer();


def writeSensor(sensor, data, now):
    cwd = os.getcwd()

    year = now.strftime("%y")
    if not os.path.isdir(year):
        os.mkdir(year)
    os.chdir(year)

    month = now.strftime("%m")
    if not os.path.isdir(month):
        os.mkdir(month)
    os.chdir(month)
 
    day = now.strftime("%d")
    if not os.path.isdir(day):
        os.mkdir(day)
    os.chdir(day)


    myfile ="%s.csv" % sensor
    with open(myfile, 'a+', newline='') as csvfile:
         datawriter = csv.writer(csvfile, delimiter=',',
                      quotechar='|', quoting=csv.QUOTE_MINIMAL)
         now = now.strftime("%H:%M:%S")
         datawriter.writerow([now, data])

    os.chdir(cwd)

def parseRow(row):
    rowcontent = row.split("!")[0]
    rowsplited = rowcontent.split(" ")
    sensor = rowsplited[0]
    rowsplited = rowsplited[1:]
    now = datetime.now()
    for mycol in rowsplited:
      #print(mycol)
      sensordata = mycol.split(":")
      sensorItem = "%s_%s" % (sensor,sensordata[0])
      writeSensor(sensorItem, int(sensordata[1]), now) 

#AckBuffer = bytearray("ACK9",'ascii')
#radio.writeAckPayload(1,AckBuffer)

while(1):   
    
    #AckBuffer = bytearray("ACK9",'ascii')
    #radio.writeAckPayload(1,AckBuffer)

    if radio.available():   
        lenmsg = radio.getDynamicPayloadSize()
        receive_payload = radio.read(lenmsg)
        try:
            a = receive_payload.decode('ascii')
            #a = a.replace("\x00\x00","")
            print(a)
            start = timer();
            GPIO.output(5, False)
            parseRow(a)
        except e:
            print("An exception occurred" + e)
    else:
        end = timer();

    if ((end-start) > 15* 60):
        print("Sound Alarm") 
        GPIO.output(5, True)	
