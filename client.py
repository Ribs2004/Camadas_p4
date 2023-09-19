from enlace import *
import time
import numpy as np

serialName = "COM6"

class datagrama(object):
    def __init__(self, b):
        self.txBuffer = b
        self.i = 1
        self.j = 1
        self.number = 16
        self.t = False
    
    def body(self):
            string_50 = b''
            first_50 = self.txBuffer[0:50]
            self.txBuffer = self.txBuffer[50:]
            string_50 += first_50
            return string_50
    
    def head(self):
            head = b''
            i_binary = self.i.to_bytes(1, 'little')
            head += i_binary
            next_10 = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            head += next_10
            if len(self.txBuffer) >= 50:
                head += self.number.to_bytes(1, 'little')
                #self.txBuffer = self.txBuffer[50:]
            else:
                head += len(self.txBuffer).to_bytes(1, 'little')
            return head

    def eop(self):
            eop = b'\xff\xff\xff'
            return eop
    
    def pacote(self):
            pack = b''
            bodyzada = self.body()
            headzada = self.head()
            eopzada = self.eop()
            pack += headzada + bodyzada + eopzada
            return pack
    
    def handshake(self):
        handshake = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF'
        print('Entrou na função Handshake')
        return handshake
         

def main():
    try:
        print("Iniciou o main")
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
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


        protocolo = datagrama(b)

        esperando_contato = True
        while esperando_contato is True:
            com1.sendData(protocolo.handshake())
            bufferLen = com1.rx.getBufferLen()
            rxBuffer, nRx = com1.getData(bufferLen)
            time.sleep(2)
            com1.rx.clearBuffer()
            if rxBuffer == b'\xCC':
                protocolo.t = True
                esperando_contato = False
            
        
        first_time = True
        while protocolo.t is True:
            bufferLen = com1.rx.getBufferLen()
            rxBuffer, nRx = com1.getData(bufferLen)
            com1.rx.clearBuffer()
            time.sleep(.5)
            print(f'rxBuffer: {rxBuffer}')
            if len(protocolo.txBuffer) >= 0 and (rxBuffer == b'\xAA' or first_time is True):
                first_time = False
                rxBuffer = 0
                pack = protocolo.pacote()
                com1.sendData(np.asanyarray(pack))
                time.sleep(.5)
                protocolo.i += 1
                protocolo.j += 1
            elif rxBuffer == b'\xBB':
                 print('Comunicação mal sucedida!')
                 protocolo.t = False
            elif len(protocolo.txBuffer) == 0:
                com1.sendData(b'\xEE')
                print('mandou a imagem completa\nComunicação Encerrada!')
                protocolo.t = False

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
        #txSize = com1.tx.getStatus()
        #print('enviou = {} comandos' .format(enviados))

        print('estou esperando')
        time.sleep(5)

        if com1.rx.getBufferLen() == 0:
            print('Time out! Comunicação encerrada!')
            com1.disable()

        rxBuffer, nRx = com1.getData(1)

        rxNumero = int.from_bytes(rxBuffer, "little")
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
if __name__ == "__main__":
    main()