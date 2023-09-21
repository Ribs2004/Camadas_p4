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
            first_114 = self.txBuffer[0:114]
            self.txBuffer = self.txBuffer[114:]
            string_114 += first_114
            return string_114
    
    def head(self, tipo):
            head = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'          
            if tipo == 1:
                head[0] = b'\x01'
                head[1] = b'\xff'
                head[3] = self.payload.to_bytes(1, 'little')
            elif tipo == 3:
                head[0] = b'\x03'
                head[3] = self.payload.to_bytes(1, 'little')
                head[4] = self.i.to_bytes(1, 'little')
            elif tipo == 5:
                head[0] = b'\x05'
            return head

    def eop(self):
            eop = b'\xaa\xbb\xcc\xdd'
            return eop
    
    def pacote(self, tipo):
            pack = b''
            bodyzada = self.body()
            headzada = self.head(tipo)
            eopzada = self.eop()
            pack += headzada + bodyzada + eopzada
            return pack
    
    def handshake(self):
        handshake = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF'
        print('Entrou na função Handshake')
        return handshake
    
    def activate_timer(self):
        return time.time()

    def elapsed_time(self, start_time):
        if start_time != None:
            elapsed_seconds = time.time() - start_time
            return elapsed_seconds
        