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
    

while server.t is True:

    bufferLen = com1.rx.getBufferLen()
    server.rxBuffer, nRx = com1.getData(bufferLen)
    time.sleep(.05)
    com1.rx.clearBuffer()
    #print(server.rxBuffer)

    """if len(server.rxBuffer) > 0:
        if server.i > server.rxBuffer[3]:
            print('Sucesso') 
            server.t = False
            break"""

    if len(server.photo) == 800:
        print('Sucesso')
        server.t = False


    timer1 = server.activate_timer()
    timer2 = server.activate_timer()       

    if len(server.rxBuffer) == 0:
        time.sleep(1)
        if server.elapsed_time(timer2) > 20:
            server.esperando = True
            pack = server.pacote(5)
            com1.sendData(pack)
            com1.disable()
            print(':-(')

        elif server.elapsed_time(timer1) > 2:
            server.pacote(4)
            com1.sendData(pack)
            timer1 = server.activate_timer()
    else:
        if server.rxBuffer[4] == server.i and server.rxBuffer[-4:] == b'\xaa\xbb\xcc\xdd':
            print('entrei')
            pack = server.pacote(4)
            com1.sendData(pack)
            time.sleep(0.5)
            print(server.rxBuffer)
            server.i += 1
            server.rxBuffer = server.rxBuffer[10:]
            server.rxBuffer = server.rxBuffer[:-4]
            server.photo += server.rxBuffer
            #print(server.photo)
            print(len(server.photo))
            print('sai')

        else:
            pack = server.pacote(6)
            com1.sendData(pack)

time.sleep(2)
print(server.photo)
print(len(server.photo))
with open('img_recebida.jpg', 'wb') as f:
    f.write(server.photo)

com1.disable()