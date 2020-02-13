import socket
import sys


class Server(object):

    def __init__(self, host='', port=9999):
        self.host = host
        self.port = port
        self.sock = None

    def create_socket(self):
        try:
            self.sock = socket.socket()
            print("Socket created...")
        except socket.error as e:
            print("Error in socket creation:", e)
            sys.exit()

    def bind_socket(self):
        try:
            if not self.sock:
                self.create_socket()

            self.sock.bind((self.host, self.port))
            print(f"Socket bound to {self.host} and {self.port}...")
            self.listen()
        except socket.error as e:
            print("Error in socket binding:", e)
            sys.exit()

    def listen(self, connection_count=5):
        if not self.sock:
            self.create_socket()
            self.bind_socket()

        self.sock.listen(connection_count)

    def accept_conn(self):
        if not self.sock:
            self.create_socket()
            self.bind_socket()
            self.listen()
        conn, address = self.sock.accept()
        print(f"Connection has been established for IP:{address[0]} and Port:{address[1]}...")
        self.send_command(conn)
        conn.close()

    def send_command(self, connection):
        while True:
            cmd = input(">$ ")
            if cmd == 'quit':
                connection.close()
                self.sock.close()
                sys.exit()
            cmd_bytes = str.encode(cmd)
            if len(cmd_bytes) > 0:
                connection.send(cmd_bytes)
                resp = str(connection.recv(1024), "utf-8")
                print(resp)
    
    def __del__(self):
        if self.sock:
            self.sock.close()


def main():
    s = Server()
    s.create_socket()
    s.bind_socket()
    s.listen()
    s.accept_conn()

if __name__ == "__main__":
    main()
