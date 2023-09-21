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
        head = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  
        if tipo == 2:
            head[0] = b'\x02'
        if tipo == 4:
            head[0] = b'\x04'
            head[7] = self.i.to_bytes(1, 'little')
        if tipo == 6:
            head[0] = b'\x06'
            head[6] = self.i.to_bytes(1, 'little')       
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
        

        