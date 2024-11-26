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
