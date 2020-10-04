import threading
import socket
import sys
import os


help = '''FNmap 1.0 - Flash Nmap (@shelld3v)
Usage: %prog {target} {options}

Options: 
 - FNmap is the same as Nmap, it accepts any Nmap options, but must be added after the {target} argument
 - To setup ports to scan, you can edit the maxium port in max_port.txt

Disclaimer: FNmap dooesn't accept IP ranges, FNmap first agrument must be a hostname or an IP address'''

class Program(object):
    def __init__(self, host, args):
        self.host = host
        self.args = args
        self.open = []
        self.resolver()

        try:
            self.maxport = int(open('max_port.txt', 'r').read().strip())
        except:
            print('Invalid maxium port number in max_port.txt')
            exit(1)

        self.setupScanner()
        self.nmap()


    def nmap(self):
        try:
            os.system('nmap -A -p {0} {1} {2}'.format(','.join(map(str, self.open)), self.host, self.args))
        except KeyboardInterrupt:
            exit(1)


    def resolver(self):
        try:
            ip = socket.gethostbyname(self.host)
        except Exception:
            print('Unable to resolve "{}"'.format(self.host))
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

            for port in range(1, self.maxport + 1):
                _thread = threading.Thread(target=self.port_scan, args=[port])
                threads.append(_thread)

            for i in range(self.maxport):
                threads[i].start()

            for i in range(self.maxport):
                if threads[i].isAlive():
                    threads[i].join()

        except KeyboardInterrupt:
            exit(1)


if __name__ == "__main__":
    if sys.argv[1] == '-h':
        print(help)
        exit(0)

    try:
        host = sys.argv[1]
    except Exception:
        print(help)
        exit(0)

    try:
        args = ' '.join(sys.argv[2:])
    except:
        args = ''

    main = Program(host, args)
