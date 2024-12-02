import socketserver
import time
import sys

from functions import *

cmd_device = [
    '?',
    'help',
    'getphonenum {name} {PIN}',
    'exit'
]

db = None

def main_loop(socket_conn, db_conn, client_address, curr_device, curr_num):
    receive_data = socket_conn.recv(2048).decode().split('\r\n')[0]

    if not curr_num:
        if receive_data == '?' or receive_data == 'help' or receive_data == 'ls':
            feedback_data = 'Available commends: \n\t' + '\n\t'.join(cmd_device)
        elif receive_data == 'exit':
            feedback_data = 'disconnected'
        else:
            cmd = receive_data.split(' ')
            if cmd[0] == 'createdevice':
                curr_device, feedback_data = device_add(db_conn, cmd[1])
            elif cmd[0] == 'getphonenum':
                curr_num, feedback_data = reg_phone_num(db_conn, cmd[1], cmd[2], curr_device)

    

    socket_conn.sendall(feedback_data.encode('UTF-8'))
    if feedback_data == 'disconnected':
        return False, None, None
    return True, curr_device, curr_num


class Server(socketserver.BaseRequestHandler):

    def handle(self):
        curr_device = None
        curr_num = None
        while True:
            conn = self.request
            addr = self.client_address
            try:
                connect, curr_device, curr_num = main_loop(conn, db, addr, curr_device, curr_num)
                if not connect:
                    print(f"{addr} closed connection.")
                    break
            except ConnectionAbortedError as e:
                print(f"{addr} closed connection.")
                break
    

if __name__ == '__main__':
    host = 'localhost'
    port = 5555
    db = conn_db()
    try:
        socket_server = socketserver.ThreadingTCPServer((host,port), Server)
        socket_server.serve_forever()
    except KeyboardInterrupt:
        sys.exit()