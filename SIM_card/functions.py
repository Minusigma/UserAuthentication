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
from server import Server

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
    create_table(conn)
    print("Connect Succeed.")
    return conn

def close_db(conn):
    conn.close()
    print("Connection closed.")

def execute_sql(conn, cmd):
    cur = conn.cursor()
    cur.execute(cmd)
    print("Executed succeed.")


def create_table(conn):
    sql1 = """CREATE TABLE IF NOT EXISTS device_info(
            DeviceNum INT PRIMARY KEY NOT NULL,
            PhoneNum INT);"""
    sql2 = """CREATE TABLE IF NOT EXISTS phone_number(
            PhoneNum INT PRIMARY KEY NOT NULL,
            Name VARCHAR(20),
            PIN INT);"""
    sql3 = """CREATE TABLE IF NOT EXISTS user_info(
            UserID SERIAL PRIMARY KEY NOT NULL,
            Name VARCHAR(20) NOT NULL,
            PhoneNum INT UNIQUE);"""
    sql4 = """CREATE TABLE IF NOT EXISTS website_info(
            ID SERIAL PRIMARY KEY NOT NULL,
            UserName VARCHAR(20) NOT NULL,
            Password VARCHAR(20) NOT NULL,
            PhoneNum INT);"""
    sql5 = """CREATE TABLE IF NOT EXISTS call_record(
            Caller INT NOT NULL,
            Callee INT NOT NULL,
            Time TIMESTAMP NOT NULL);"""
    execute_sql(conn, sql1)
    execute_sql(conn, sql2)
    execute_sql(conn, sql3)
    execute_sql(conn, sql4)
    execute_sql(conn, sql5)

def create_device(conn):
    device_num = random.randint(100, 1000)
    conn.send(f"createdevice {device_num}".encode('UTF-8'))
    conn.recv(2048).decode()
    return device_num

def device_add(db_conn, d_num):
    sql = """INSERT INTO device_info (DeviceNum, PhoneNum) VALUES (%s, %s);"""
    d_num = int(d_num)
    param = (d_num, None)
    cur = db_conn.cursor()
    cur.execute(sql, param)
    db_conn.commit()
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

def reg_phone_num(db_conn, name, pin, device):
    cur = db_conn.cursor()
    sql1 = """SELECT PhoneNum FROM phone_number WHERE name is null;"""
    cur.execute(sql1)
    db_conn.commit()
    phone_list = cur.fetchall()
    phone_num = phone_list[random.randint(0, len(phone_list) - 1)][0]
    sql2 = """UPDATE phone_number SET name = %s, pin = %s WHERE PhoneNum = %s;"""
    param = (name, pin, phone_num)
    cur.execute(sql2, param)
    db_conn.commit()
    sql3 = """UPDATE device_info SET PhoneNum = %s WHERE DeviceNum = %s;"""
    param = (phone_num, device)
    cur.execute(sql3, param)
    db_conn.commit()
    return phone_num, 'Register succeed.'

def make_call(db_conn, caller, callee):
    cur = db_conn.cursor()
    sql = """INSERT INTO call_record (caller, callee, time) VALUES (%s, %s, %s);"""
    param = (caller, callee, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    cur.execute(sql, param)
    db_conn.commit()
    return 'Call succeed.'

def delete_phone_num(db_conn, phone_num):
    cur = db_conn.cursor()
    sql = """UPDATE phone_number SET name = NULL, pin = NULL WHERE number = %s;"""
    param = (phone_num)
    cur.execute(sql, param)
    db_conn.commit()
    sql2 = """UPDATE device_info SET phone_num = NULL WHERE phone_num = %s;"""
    param = (phone_num)
    cur.execute(sql2, param)
    db_conn.commit()
    return 'Delete succeed.'

def register_user(db_conn, name, password, phone_num):
    cur = db_conn.cursor()
    sql = """SELECT * FROM website_info WHERE UserName = %s;"""
    param = (name,)
    cur.execute(sql, param)
    db_conn.commit()
    user_name = cur.fetchall()
    if len(user_name) != 0:
        return 'User already exists.'
    sql1 = """SELECT * FROM phone_number WHERE PhoneNum = %s;"""
    param = (phone_num,)
    cur.execute(sql1, param)
    db_conn.commit()
    list = cur.fetchall()
    if len(list) == 0:
        return 'Phone number does not exist.'
    sql2 = """INSERT INTO website_info (UserName, Password, PhoneNum) VALUES (%s, %s, %s);"""
    param = (name, password, phone_num)
    cur.execute(sql2, param)
    db_conn.commit()
    return 'Register succeed.'

def login_by_name_password(db_conn, name, password):
    cur = db_conn.cursor()
    sql = """SELECT * FROM website_info WHERE UserName = %s;"""
    param = (name)
    cur.execute(sql, param)
    db_conn.commit()
    list = cur.fetchall()
    if len(list) == 0:
        return 'No such user.'
    if list[0][2] != password:
        return 'Wrong password.'
    return 'Login succeed.'



def login_by_phone_password(db_conn, phone_num, password):
    cur = db_conn.cursor()
    sql = """SELECT * FROM website_info WHERE PhoneNum = %s;"""
    param = (phone_num)
    cur.execute(sql, param)
    db_conn.commit()
    list = cur.fetchall()
    if len(list) == 0:
        return 'No such user.'
    if list[0][2] != password:
        return 'Wrong password.'
    return 'Login succeed.'

def login_by_phone_pin(db_conn, phone_num):
    cur = db_conn.cursor()
    sql = """SELECT * FROM website_info WHERE PhoneNum = %s;"""
    param = (phone_num,)
    cur.execute(sql, param)
    db_conn.commit()
    list = cur.fetchall()
    if len(list) == 0:
        return None, 'No such user.'
    name = list[0][0]
    pin = random.randint(1000, 9999)
    sql2 = """SELECT DeviceNum FROM device_info WHERE PhoneNum = %s;"""
    param = (phone_num)
    cur.execute(sql2, param)
    db_conn.commit()
    device_num = cur.fetchall()[0][0]
    if device_num in Server.tcp_conns:
        tcp_conn = Server.tcp_conns[device_num]
        tcp_conn.send(f'pin {pin}'.encode())
    feedback = tcp_conn.recv(2048).decode()
    if feedback == pin:
        return name,'Login succeed.'
    return None,'Wrong PIN.'

def logout():
    return None, 'Logout succeed'

def change_device(db_conn, tcp_conn, device_num, phone_num, password, curr_num):
    tcp_conns = Server.tcp_conns
    cur = db_conn.cursor()
    sql = """SELECT * FROM device_info WHERE PhoneNum = %s;"""
    param = (phone_num,)
    cur.execute(sql, param)
    db_conn.commit()
    list = cur.fetchall()
    if len(list) == 0:
        return curr_num, 'No such user.'
    origin_device = list[0][0]
    print(f"origin_device: {origin_device}, device_num: {device_num}")
    if origin_device == device_num:
        return curr_num, 'Already in this device.'
    if origin_device in tcp_conns.keys():
        origin_tcp = tcp_conns[origin_device]
    else:
        origin_tcp = None
    sql2 = """SELECT * FROM phone_number WHERE PhoneNum = %s;"""
    param = (phone_num,)
    cur.execute(sql2, param)
    db_conn.commit()
    list = cur.fetchall()
    print(f"password type: {type(password)}, value: {password}")
    print(f"stored password type: {type(list[0][2])}, value: {list[0][2]}")
    if password == str(list[0][2]):
        if origin_tcp:
            origin_tcp.send(f'logout {phone_num}')
        sql2 = """UPDATE device_info SET PhoneNum = NULL WHERE DeviceNum = %s;"""
        param = (origin_device,)
        cur.execute(sql2,param)
        db_conn.commit()
        sql3 = """UPDATE device_info SET PhoneNum = %s WHERE DeviceNum = %s;"""
        param = (phone_num, device_num)
        cur.execute(sql3, param)
        db_conn.commit()
        return phone_num,'Change device succeed.'
    else:
        tcp_conn.send(f'Please print the last two calls'.encode('UTF-8'))
        feedback = tcp_conn.recv(2048).decode().split(' ')
        print(feedback)
        sql3 = """SELECT * FROM call_record WHERE caller = %s ORDER BY time DESC LIMIT 2;"""
        param = (phone_num,)
        cur.execute(sql3, param)
        db_conn.commit()
        call_record = cur.fetchall()
        if len(call_record) == 2:
            if (str(call_record[0][1]) == feedback[0] and str(call_record[1][1]) == feedback[1]) or (str(call_record[0][1]) == feedback[1] and str(call_record[1][1]) == feedback[0]):
                sql4 = """UPDATE device_info SET PhoneNum = NULL WHERE DeviceNum = %s;
                UPDATE device_info SET PhoneNum = %s WHERE DeviceNum = %s;"""
                param = (origin_device, phone_num, device_num)
                cur.execute(sql4, param)
                db_conn.commit()
                return phone_num, 'Change device succeed.'
    return curr_num, 'Change device failed.'



