from functions import *
import time
import threading

def receive_messages(client):
    while True:
        try:
            recv_data = client.recv(2048)
            if not recv_data:
                continue
            print(f"\nServer:\n{recv_data}")
            if recv_data == 'disconnected':
                break
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
        established_client.send(f'createdevice {device_num}')
        
        while True:
            try:
                cmd = input().strip()
                if not cmd:
                    continue
                established_client.send(cmd)
            except:
                break
                
        established_client.close()
    print('Goodbye')