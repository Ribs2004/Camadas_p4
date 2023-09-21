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

def handshake():
    com1.sendData(b'\xCC')

def receivedOK():
    com1.sendData(b'\xAA')

def receivedNotOK():
    com1.sendData(b'\xBB')


while server.esperando is True:

    bufferLen = com1.rx.getBufferLen()
    server.rxBuffer, nRx = com1.getData(bufferLen)
    com1.rx.clearBuffer()

    if server.rxBuffer[0] == b'\x01' and server.rxBuffer[1] == b'\xff':
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

    if server.rxBuffer[0] >= server.i:
        print('Sucesso') 

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
            pack = server.pacote(4)
            com1.sendData(pack)
            server.i += 1
        else:
            pack = server.pacote(6)
            com1.sendData(pack)
            

    



    

    
    
    








server.t = True
first_time = True
while server.t:

    # PEGAR TUDO QUE TEM NO BUFFER, SALVAR NA VARIÁVEL RXBUFFER, APAGAR O QUE TEM NO BUFFER E DEPOIS ESPERAR 0.5s

    bufferLen = com1.rx.getBufferLen()
    server.rxBuffer, nRx = com1.getData(bufferLen)
    com1.rx.clearBuffer()
    time.sleep(.5)
    print('primeiro print', server.rxBuffer)

    if server.rxBuffer == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff' and first_time is True:
        handshake()
        first_time = False
        print("Mandei o Handshake")
        server.rxBuffer = 1
    elif len(server.rxBuffer) != 0:
        if server.rxBuffer[0] == 238:
            print('imagem finalizada')
            server.t = False
        if server.rxBuffer[0] == server.i: 
            x = server.rxBuffer[11]  
            server.rxBuffer = server.rxBuffer[12:-3]
            if len(server.rxBuffer) != x:          #.from_bytes(1, 'little')
                print('Tamanhos Diferentes')
                server.t = False
            server.photo += server.rxBuffer 
            server.i += 1
            receivedOK()
            time.sleep(.25)
        else:
            receivedNotOK()
            break
    print(len(server.photo))
    rxBuffer = 0

time.sleep(2)
with open('img_recebida.jpg', 'wb') as f:
    f.write(server.photo)

com1.disable()