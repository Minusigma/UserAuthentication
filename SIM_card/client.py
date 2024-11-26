from functions import *
import time

if __name__ == '__main__':
    print("Simulation started.")
    established_client, info = tcp_conn()
    print(info)

    if established_client:
        device_num = create_device(established_client)
        while True:
            cmd = input().strip()
            if not cmd:
                continue
            established_client.send(cmd)

            recv_data = established_client.recv(2048)

            print(f"Server:\n{recv_data}")
            if recv_data == 'disconnected':
                break
        established_client.close()
    print('Goodbye')