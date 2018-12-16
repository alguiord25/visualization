#!/usr/bin/env python3

##Raspberry Pi receiver

from RF24 import *
#import spidev

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

while(1):    
    if radio.available():    
        len = radio.getDynamicPayloadSize()
        receive_payload = radio.read(len)
        print(receive_payload)
