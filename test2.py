import socket
from multiprocessing import Process, Pipe
from threading import Thread
import time
import sys
from datetime import datetime



class Server(Thread):
    def __init__(self, end, port):
        Thread.__init__(self)
        self.end = end
        self.port = port


    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server started successfully\n")
        hostname = ''
        port = self.port
        self.sock.bind((hostname, port))
        self.sock.listen(1)
        print("Listening on port %d\n" % port)
        # time.sleep(2)
        (clientname, address) = self.sock.accept()
        print("Connection from %s\n" % str(address))
        while 1:
            chunk = clientname.recv(4096)
            buf = self.end.recv()
            print(buf)
            print('\n' + str(address) + '-', buf, ':' + str(chunk, encoding='UTF-8'))







class Client(Thread, *sys.argv[1:]):
    def __init__(self,end):
        Thread.__init__(self)
        self.end = end


    def connect(self, host, port):
        self.sock.connect((host, port))


    def client(self, host, port, msg, ):
        sent = self.sock.send(bytes(msg, encoding='UTF-8'))
        buf = self.end.recv()
        print("YOU " , buf, ':' + msg)


    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            host = input("Enter the hostname\n>>")
            port = int(input("Enter the port\n>>"))
        except EOFError:
            print('err')
            return 1

        print("Connecting\n")
        s = ''
        self.connect(host, port)
        print("Connected\n")
        while 1:
            #"Waiting for message\n"
            msg = input('>>')
            if msg == '!exit!':
                break
            if msg == '':
                continue
           # print("Sending\n")
            self.client(host, port, msg)
        return (1)
class Net(Process):
    def __init__(self, end, port):
        Process.__init__(self)
        self.end = end
        self.port = port
    def run(self):
        sys.stdin = open(0)
        srv = Server(self.end, self.port)
        srv.daemon = True
        print("Starting server")
        srv.start()
        time.sleep(1)
        print("Starting client")
        cli = Client(self.end)
        cli.start()
        print("Started successfully")



class Time(Process):
    def __init__(self, begin):
        Process.__init__(self)

        self.begin = begin
    def sd(self, date):
        self.begin.send(date)
    def run(self):

        while True:
            timeval = datetime.now()
            time.sleep(1)
            self.sd(timeval)
        self.begin.close()






if __name__ == '__main__':
    port = int(input("Input port: "))
    print('\n')
    end, begin = Pipe()
    nt = Net(end, port)
    nt.start()
    tm = Time(begin)
    tm.start()
    nt.join()
    tm.join()







