import socket
from typing import NoReturn


class Server:
    def __init__(self, ip: str, port: int) -> NoReturn:
        self.ip = ip
        self.port = port

    def start_connection(self) -> NoReturn:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            s.listen()
            conn, _ = s.accept()
            k = int.from_bytes(conn.recv(4), "big")



server = Server("127.0.0.1", 6000)
server.start_connection()
