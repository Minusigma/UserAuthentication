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

DATABASE = "userauth"
USER = "admin"
PASSWORD = "123456"
HOST = "localhost"
PORT = "5432"
SERVER_IP = 'localhost'
SERVER_PORT = '5555'

def conn_db():
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD, 
                            host=HOST, 
                            port=PORT)
    
    # cur = conn.cursor()
    # cur.execute('''CREATE TABLE device_info(
    #            DeviceNum INT PRIMARY KEY NOT NULL,
    #            PhoneNum INT NOT NULL)''')
    # conn.commit()
    print("Connect Succeed.")
    # conn.close()
    return conn

def close_db(conn):
    conn.close()
    print("Connection closed.")

def execute_sql(conn, cmd):
    cur = conn.cursor()
    cur.execute(cmd)
    print("Executed succeed.")


def create_device(conn):
    device_num = random.randint(100, 1000)
    conn.send(f"createdevice {device_num}")
    conn.recv(2048)
    return device_num

def device_add(db_conn, d_num):
    sql = """INSERT INTO device_info (device_num, phone_num) VALUES (%d, %d);"""
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

def get_phone_num(db_conn, name, pin, device):
    cur = db_conn.cursor()
    sql1 = """SELECT number FROM phone_number WHERE name is null;"""
    cur.execute(sql1)
    db_conn.commit()
    phone_list = cur.fetchall()
    return NotImplemented