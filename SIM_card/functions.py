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
