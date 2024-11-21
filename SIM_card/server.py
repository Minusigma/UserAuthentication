import socketserver
import asyncio
import time

from functions import *

def main_loop(socket_conn, client_address, login_user):
    print("conn")

class Server(socketserver.BaseRequestHandler):
    def __init__(self):
        self.conn = set()

    async def handle(self):
        try:
            self.conn.add()
    

if __name__ == '__main__':
    host = 'localhost'
    port = 5555
    try:

    except KeyboardInterrupt:
        pass