import threading
from enlace import *
import numpy as np

serialName = "COM6"

com1 = enlace(serialName)

com1.enable()
print("esperando 1 byte de sacrifício")
rxBuffer, nRx = com1.getData(1)
com1.rx.clearBuffer()
time.sleep(.1)

def handshake():
    com1.sendData(b'\xCC')

def receivedOK():
    com1.sendData(b'\xAA')

def receivedNotOK():
    com1.sendData(b'\xBB')

i = 1
t = True
photo = b''
first_time = True
while t:
    bufferLen = com1.rx.getBufferLen()
    rxBuffer, nRx = com1.getData(bufferLen)
    com1.rx.clearBuffer()
    time.sleep(.5)
    print('primeiro print', rxBuffer)
    if rxBuffer == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff' and first_time is True:
        handshake()
        first_time = False
        print("Mandei o Handshake")
        rxBuffer = 1
    elif len(rxBuffer) != 0:
        if rxBuffer[0] == 238:
            print('imagem finalizada')
            t = False
        if rxBuffer[0] == i: 
            x = rxBuffer[11]  
            rxBuffer = rxBuffer[12:-3]
            if len(rxBuffer) != x:          #.from_bytes(1, 'little')
                print('Tamanhos Diferentes')
                t = False
            photo += rxBuffer 
            i += 1
            receivedOK()
            time.sleep(.25)
        else:
            receivedNotOK()
            break
    print(len(photo))
    rxBuffer = 0

time.sleep(2)
with open('img_recebida.jpg', 'wb') as f:
    f.write(photo)

com1.disable()