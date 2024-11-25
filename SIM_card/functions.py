import hmac
import os
import socket
import hashlib
import re
import random
import ast
import fileinput
import time
import psycopg2

SERVER_IP = 'localhost'
SERVER_PORT = '5555'

def conn_db():
    pass

def close_db(db):
    db.close()
    print('Database disconnected.')

def execute_sql(sql):
    pass

def create_device(conn):
    device_num = random.randint(100, 1000)
    conn.send(f"createdevice {device_num}")
    conn.recv(2048)
    return device_num

def device_add(db_conn, d_num):
    sql = """INSERT INTO device_info (device_num, phone_num) VALUES (%d, %d)"""
    param = (d_num , None)
    cur = db_conn.cursor()
    cur.execute(sql,param)
    db_conn.conmmit()
    feedback = 'Add succeed.'
    return d_num, feedback    


def tcp_conn():
    ip,port = SERVER_IP, SERVER_PORT
    port = (int) (port)
    information = 'success'
    socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        socket_client.connect((ip,port))
    except socket.error as e:
        information = (str)(e)
    return socket_client,information

def get_phone_num(db_conn, )