from enlace import *
import time
import numpy as np
from protocolo import Datagrama

serialName = "COM6"

def main():
    try:
        print("Iniciou o main")
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta

        com1 = enlace(serialName)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

        # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")

        with open('KFC_11zon.jpg', 'rb') as image:
            f = image.read()
            b = bytearray(f)

        #print(f'tamanho b: {len(b)}')
        protocolo = Datagrama(b)
        protocolo.payloads()
        #print(protocolo.payload)


        inicia = False
        while inicia is False:
            pack = protocolo.pacote(1)
            com1.sendData(pack)
            print('Mandei o pack 1')
            time.sleep(5)
            bufferLen = com1.rx.getBufferLen()
            protocolo.rxBuffer, nRx = com1.getData(bufferLen)
            com1.rx.clearBuffer()
            print(f'rxBuffer: {protocolo.rxBuffer}')
            if protocolo.rxBuffer[0] == 2:
                inicia = True


        while inicia is True:
            if protocolo.i > protocolo.payload:
                print('SUCESSO!')
                com1.disable()
            else:
                #pack = protocolo.pacote(3)
                #com1.sendData(pack)
                #print(f'pack: {pack}')
                timer1 = protocolo.activate_timer()
                timer2 = protocolo.activate_timer()

            time.sleep(2)
            bufferLen = com1.rx.getBufferLen()
            protocolo.rxBuffer, nRx = com1.getData(bufferLen)
            time.sleep(.05)
            com1.rx.clearBuffer()
            print(f'rxbuffer 4: {protocolo.rxBuffer}')

            if len(protocolo.rxBuffer) != 0:
                print('recebi alguma coisa')
                if protocolo.rxBuffer[0] == 4:
                    print('recebi 4')
                    protocolo.i += 1
                elif protocolo.rxBuffer[0] == 5:
                    com1.disable()
                    break

            else:
                print('entrei no else')
                if protocolo.elapsed_time(timer1) > 5:
                    print('pau inicial')
                    #pack = protocolo.pacote(3)
                    #com1.sendData(pack)
                    timer1 = protocolo.activate_timer()
                
                if protocolo.elapsed_time(timer2) > 20:
                    print('pauzou')
                    pack = protocolo.pacote(5)
                    com1.sendData(pack)
                    com1.disable()
                    print(':-(')
                else:
                    bufferLen = com1.rx.getBufferLen()
                    print('pau 1')
                    protocolo.rxBuffer, nRx = com1.getData(bufferLen)
                    time.sleep(.05)
                    com1.rx.clearBuffer()

                print('rolassa')
                if len(protocolo.rxBuffer) > 0:
                    if protocolo.rxBuffer[0] == 6:
                        print('pau 2')
                        protocolo.i = protocolo.rxBuffer[6].from_bytes(1, 'little')
                        pack = protocolo.pacote(3)
                        com1.sendData(pack)
                        timer1 = protocolo.activate_timer()
                        timer2 = protocolo.activate_timer()
            

        print('Loop Finalizado')

        #print(enviados)

        #print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        # faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.

        # finalmente vamos transmitir os dados. Para isso usamos a funçao sendData que é um método da camada enlace.
        # faça um print para avisar que a transmissão vai começar.
        # tente entender como o método send funciona!
        # Cuidado! Apenas trasmita arrays de bytes!

        # as array apenas como boa pratica para casos de ter uma outra forma de dados

        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar funcionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        while com1.tx.transLen == 0:
            pass
        #txSize = protocolo.com1.tx.getStatus()
        #print('enviou = {} comandos' .format(enviados))

        print('estou esperando')
        time.sleep(5)

        if com1.rx.getBufferLen() == 0:
            print('Time out! Comunicação encerrada!')
            com1.disable()

        protocolo.rxBuffer, nRx = com1.getData(1)

        rxNumero = int.from_bytes(protocolo.rxBuffer, "little")
        print('Pronto, recebi de volta {}'.format(rxNumero))

        #if enviados == rxNumero:
            #print('Comunicação feita com sucesso!')
        #else:
            #print('Comunicação não deu certo...')

        # Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        # Observe o que faz a rotina dentro do thread RX
        # print um aviso de que a recepção vai começar.

        # Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        # Veja o que faz a funcao do enlaceRX  getBufferLen

        # acesso aos bytes recebidos

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__== "__main__":
    main()