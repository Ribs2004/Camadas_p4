import threading
from enlace import *
import numpy as np
from horda_de_servos import Servidor

serialName = "COM6"

server = Servidor()
com1 = enlace(serialName)

com1.enable()
print("esperando 1 byte de sacrifício")
server.rxBuffer, nRx = com1.getData(1)
com1.rx.clearBuffer()
time.sleep(.1)

while server.esperando is True:

    bufferLen = com1.rx.getBufferLen()
    server.rxBuffer, nRx = com1.getData(bufferLen)
    com1.rx.clearBuffer()

    if len(server.rxBuffer) > 0:
        if server.rxBuffer[0] == 1 and server.rxBuffer[1] == 255:
            server.esperando = False

    time.sleep(1)

    if server.esperando is False:
        pack = server.pacote(2)
        com1.sendData(pack)
        print(pack)
        time.sleep(0.15)
    
server.rxBuffer = 0
first_time = True
while server.t is True:

    bufferLen = com1.rx.getBufferLen()
    server.rxBuffer, nRx = com1.getData(bufferLen)
    time.sleep(.05)
    com1.rx.clearBuffer()
    #print(server.rxBuffer)


    if len(server.photo) == 800:
        print('Sucesso')
        server.t = False      

    if first_time is True:
        timer1 = server.activate_timer()
        timer2 = server.activate_timer()
        first_time = False

    print(server.elapsed_time(timer1))
    print(server.elapsed_time(timer2))

    if len(server.rxBuffer) == 0:
        time.sleep(1)
        if server.elapsed_time(timer2) > 20:
            server.esperando = True
            pack = server.pacote(5)
            print(pack)
            com1.sendData(pack)
            time.sleep(.05)
            com1.disable()
            #print(':-(')
            break

        elif server.elapsed_time(timer1) > 2:
            pack = server.pacote(4)
            com1.sendData(pack)
            print(pack)
            timer1 = server.activate_timer()
    else:
        if server.rxBuffer[4] == server.i and server.rxBuffer[-4:] == b'\xaa\xbb\xcc\xdd':
            #print('entrei')
            pack = server.pacote(4)
            com1.sendData(pack)
            print(pack)
            timer1 = server.activate_timer()
            timer2 = server.activate_timer()
            time.sleep(0.5)
            #print(server.rxBuffer)
            server.i += 1
            server.rxBuffer = server.rxBuffer[10:]
            server.rxBuffer = server.rxBuffer[:-4]
            server.photo += server.rxBuffer
            #print(server.photo)
            #print(len(server.photo))
            #print('sai')

        else:
            pack = server.pacote(6)
            com1.sendData(pack)
            print(pack)
 
time.sleep(2)
print(server.photo)
print(len(server.photo))
with open('img_recebida.jpg', 'wb') as f:
    f.write(server.photo)

com1.disable()