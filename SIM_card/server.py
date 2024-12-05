import socketserver
import time
import sys

from functions import *

cmd_device = [
    '?',
    'help',
    'getphonenum {name} {PIN}',
    'changedevice {phone_num} {password}',
    'currentdevice',
    'exit'
]

cmd_phone = [
    '?',
    'help',
    'register {name} {passward} {phone_num}',
    'loginnamepwd {name} {passward}',
    'loginphonepwd {phone_num} {passward}',
    'loginphonepin {phone_num} {pin}',
    'currentinfo',
    'exit'
]
# def main_loop(socket_conn, db_conn, client_address, curr_device, curr_num, tcp_conns):
#     receive_data = socket_conn.recv(2048).decode().split('\r\n')[0]

#     if not curr_num:
#         if receive_data == '?' or receive_data == 'help' or receive_data == 'ls':
#             feedback_data = 'Available commends: \n\t' + '\n\t'.join(cmd_device)
#         elif receive_data == 'exit':
#             feedback_data = 'disconnected'
#         else:
#             cmd = receive_data.split(' ')
#             if cmd[0] == 'createdevice':
#                 curr_device, feedback_data = device_add(db_conn, cmd[1])
#                 tcp_conns[curr_device] = socket_conn
#             elif cmd[0] == 'getphonenum':
#                 curr_num, feedback_data = reg_phone_num(db_conn, cmd[1], cmd[2], curr_device)

    

#     socket_conn.sendall(feedback_data.encode('UTF-8'))
#     if feedback_data == 'disconnected':
#         return False, None, None
#     return True, curr_device, curr_num


class Server(socketserver.BaseRequestHandler):
    def __init__(self):
        self.tcp_conns = {}
        self.db = conn_db()

    def handle(self):
        curr_device = None
        curr_num = None
        connect = True
        while True:
            conn = self.request
            addr = self.client_address
            try:
                # connect, curr_device, curr_num = main_loop(conn, db, addr, curr_device, curr_num, self.tcp_conns)
                receive_data = conn.recv(2048).decode().split('\r\n')[0]
                
                if not curr_device:
                    cmd = receive_data.split(' ')
                    if cmd[0] == 'createdevice':
                        curr_device, feedback_data = device_add(db, cmd[1])
                        self.tcp_conns[curr_device] = conn
                    else:
                        feedback_data = 'Please create a device first.'
                elif not curr_num:
                    if receive_data == 'help' or receive_data == '?':
                        feedback_data = 'Available commends: \n\t' + '\n\t'.join(cmd_device)
                    elif receive_data == 'exit':
                        feedback_data = 'disconnected'
                        connect = False
                    elif receive_data == 'currentdevice':
                        feedback_data = f"Current device: {curr_device}"
                    else:
                        cmd = receive_data.split(' ')
                        if cmd[0] == 'getphonenum':
                            curr_num, feedback_data = reg_phone_num(db, cmd[1], cmd[2], curr_device)
                        elif cmd[0] == 'changedevice':
                            feedback_data = change_device(db, curr_device, cmd[1], cmd[2])
                else:
                    if receive_data == 'help' or receive_data == '?':
                        feedback_data = 'Available commends: \n\t' + '\n\t'.join(cmd_phone)
                    elif receive_data == 'exit':
                        feedback_data = 'disconnected'
                        connect = False
                    elif receive_data == 'currentinfo':
                        feedback_data = f"Current device / number: {curr_device} / {curr_num}"
                    else:
                        cmd = receive_data.split(' ')
                        if cmd[0] == 'register':
                            feedback_data = register_user(db, cmd[1], cmd[2], cmd[3])
                        elif cmd[0] == 'loginnamepwd':
                            feedback_data = login_by_name_password(db, cmd[1], cmd[2])
                        elif cmd[0] == 'loginphonepwd':
                            feedback_data = login_by_phone_password(db, cmd[1], cmd[2])
                        elif cmd[0] == 'loginphonepin':
                            feedback_data = login_by_phone_pin(db, self.tcp_conns, cmd[1])
                conn.sendall(feedback_data.encode('UTF-8'))
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