from functions import create_device, tcp_conn
import time
import threading
import sys

def receive_messages(client):
    while True:
        try:
            recv_data = client.recv(2048).decode()
            if not recv_data:
                continue
            print(f"\nServer:\n{recv_data}")
            if recv_data == 'disconnected':
                client.close()
                sys.exit(0)
        except:
            break

if __name__ == '__main__':
    print("Simulation started.")
    established_client, info = tcp_conn()
    print(info)

    if established_client:
        device_num = create_device(established_client)
        
        
        receive_thread = threading.Thread(target=receive_messages, args=(established_client,))
        receive_thread.daemon = True
        receive_thread.start()
        established_client.send(f'createdevice {device_num}'.encode('UTF-8'))
        
        while True:
            try:
                cmd = input().strip()
                if not cmd:
                    continue
                established_client.send(cmd.encode('UTF-8'))
            except:
                break
                
        established_client.close()
    print('Goodbye')