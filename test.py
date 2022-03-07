import sqlite3
import sys
import random
from functions import update_yards, get_stats, log, get_clock, update_clock
from api import api as api
import time
import os

conn = sqlite3.connect('data.db')
cur = conn.cursor()

lines = 0
file_list = []
for file in os.listdir():
    if file.endswith(".py"):
        with open(file, 'r') as files:
            for i in files:
                if len(i) > 1:
                    lines += 1
print(f"There are {lines} of code")
