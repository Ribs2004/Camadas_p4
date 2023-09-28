import time

class Datagrama(object):
    def __init__(self, b):
        self.txBuffer = b
        self.rxBuffer = 0
        self.i = 1
        self.j = 1
        self.number = 114
        self.t = False
        self.payload = 0
    
    def payloads(self):
        if len(self.txBuffer) % 114 == 0:
            self.payload = len(self.txBuffer) / 114
        else:
            self.payload = int((len(self.txBuffer) / 114)) + 1 

    def body(self):
            string_114 = b''
            print(f'len tx buffer: {len(self.txBuffer)}')
            if len(self.txBuffer) < 114:
                print('estou no 2')
                string_114 = self.txBuffer[0:len(self.txBuffer) + 1] 
            else:
                first_114 = self.txBuffer[0:114]
                self.txBuffer = self.txBuffer[114:]
                string_114 += first_114

            return string_114
    
    def head(self, tipo):
            head = b''          
            if tipo == 1:
                head += b'\x01\xff\x00'
                head += self.payload.to_bytes(1, 'little')
                head += b'\x00\x00\x00\x00\x00\x00'
            elif tipo == 3:
                head += b'\x03\x00\x00'
                head += self.payload.to_bytes(1, 'little')
                head += self.i.to_bytes(1, 'little')
                head += b'\x00\x00\x00\x00\x00'
            elif tipo == 5:
                head += b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            return head

    def eop(self):
            eop = b'\xaa\xbb\xcc\xdd'
            return eop
    
    def pacote(self, tipo):
            pack = b''
            if tipo != 1 and tipo != 5:
                bodyzada = self.body()
            headzada = self.head(tipo)
            eopzada = self.eop()

            if tipo == 1 or tipo == 5:
                pack += headzada + eopzada
            else:
                pack += headzada + bodyzada + eopzada
            print("acabou")
            return pack
    
    def handshake(self):
        handshake = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff'
        print('Entrou na função Handshake')
        return handshake
    
    def activate_timer(self):
        return time.time()

    def elapsed_time(self, start_time):
        if start_time != None:
            elapsed_seconds = time.time() - start_time
            return elapsed_seconds