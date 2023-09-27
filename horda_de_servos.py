import time

class Servidor(object):
    def __init__(self):
        self.txBuffer = 0
        self.rxBuffer = 0
        self.i = 1
        self.j = 1
        self.number = 114
        self.t = True
        self.photo = b''
        self.esperando = True

    
    def head(self, tipo):
        head = b''  
        if tipo == 2:
            head += b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        if tipo == 4:
            head += b'\x04\x00\x00\x00\x00\x00'
            head += self.i.to_bytes(1, 'little')
            head += b'\x00\x00\x00'
        if tipo == 5:
            head += b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        if tipo == 6:
            head += b'\x05\x00\x00\x00\x00'
            head += self.i.to_bytes(1, 'little')   
            head += b'\x00\x00\x00\x00'    
        return head

    def eop(self):
        eop = b'\xaa\xbb\xcc\xdd'
        return eop
    
    def pacote(self, tipo):
        pack = b''
        headzada = self.head(tipo)
        eopzada = self.eop()
        pack += headzada + eopzada
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
        

        