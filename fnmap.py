import threading
import socket
import sys
import os


class Program(object):
    def __init__(self, host, args):
        self.host = host
        self.args = args
        self.open = []
        self.setupScanner()
        self.nmap()


    def nmap(self):
        try:
            os.system('nmap -A -p {0} {1} {2}'.format(','.join(map(str, self.open)), self.host, self.args))
        except KeyboardInterrupt:
            exit(1)


    def port_scan(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(2)

        try:
            s.connect((self.host, port))
            self.open.append(str(port))
            s.close()

        except Exception:
            pass


    def setupScanner(self):
        try:
            
            threads = []

            for port in range(1, 65536):
                _thread = threading.Thread(target=self.port_scan, args=[port])
                threads.append(_thread)

            for i in range(65535):
                threads[i].start()

            for i in range(65535):
                if threads[i].isAlive():
                    threads[i].join()

        except KeyboardInterrupt:
            exit(1)


if __name__ == "__main__":
    try:
        host = sys.argv[1]
    except Exception:
        print('%prog <target> <options>')

    try:
        args = ' '.join(sys.argv[2:])
    except:
        args = ''

    main = Program(host, args)
