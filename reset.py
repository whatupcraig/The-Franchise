import sqlite3
from api import api as api
import sys
import easygui as e
import time


def reset_season_meta():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT user FROM Season")
    data = cur.fetchall()
    for user in data:
        username = user[0]
        api.set_metadata('Overall', 60, username)
        api.set_metadata('Offense', 60, username)
        api.set_metadata('Defense', 60, username)
        api.set_metadata('Rush Offense', 60, username)
        api.set_metadata('Pass Offense', 60, username)
        api.set_metadata('Rush Defense', 60, username)
        api.set_metadata('Pass Defense', 60, username)
        api.set_metadata('Special Teams', 60, username)
        api.set_metadata('Wins', 0, username)
        api.set_metadata('Losses', 0, username)
        api.set_metadata('Ties', 0, username)
        api.set_metadata('Interceptions', 0, username)
        api.set_metadata('Sacks', 0, username)
        api.set_metadata('Fumbles', 0, username)
        time.sleep(.5)


def reset_meta():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT user FROM Record")
    data = cur.fetchall()
    for user in data:
        username = user[0]
        api.set_metadata('All Time Wins', 0, username)
        api.set_metadata('All Time Losses', 0, username)
        api.set_metadata('All Time Ties', 0, username)
        api.set_metadata('Championships', 0, username)
        api.set_metadata('Grade', 'C', username)
        time.sleep(.5)


def create_tables():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Season  (
                user text,
                overall integer,
                offense integer,
                defense integer,
                rush_offense integer,
                pass_offense integer,
                rush_defense integer,
                pass_defense integer,
                special_teams integer,
                games integer,
                wins integer,
                losses integer,
                ties integer
                )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Record  (
                user text,
                wins integer,
                losses integer,
                ties integer,
                games integer,
                grade text
                )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Stats  (
                user text,
                games integer,
                ypg integer,
                ppg integer,
                yapg integer,
                papg integer,
                turnovers integer,
                pass_ypg integer,
                rush_ypg integer,
                pass_apg integer,
                rush_apg integer,
                sacks integer,
                interceptions integer,
                fumbles integer
                )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Games  (
                player_one text,
                player_two text,
                player_one_score integer,
                player_two_score integer,
                yards integer,
                points integer,
                turnovers integer
                )''')
    conn.close()
    api.chat_feed_alert("Franchise Tables Created")


def reset_season():
    reset_season_meta()
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    try:
        cur.execute("DROP TABLE IF EXISTS Season;")
        cur.execute("DROP TABLE IF EXISTS Stats;")
        cur.execute("DROP TABLE IF EXISTS Games;")
        api.chat_feed_alert("Franchise Season Reset")
    except:
        pass
    create_tables()
    api.remove_allrole('Franchise')
    api.bot_chat('Franchise season has been reset')

def reset_all():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    reset_season_meta()
    reset_meta()
    try:
        cur.execute("DROP TABLE IF EXISTS Season;")
        cur.execute("DROP TABLE IF EXISTS Stats;")
        cur.execute("DROP TABLE IF EXISTS Games;")
        cur.execute("DROP TABLE IF EXISTS Record;")
        api.chat_feed_alert("Franchise All Reset")
    except:
        pass
    create_tables()
    api.remove_allrole('Franchise')


data = sys.argv

if int(data[1]) == 1:
    confirm = e.ccbox('Reset Season')
    if confirm == True:
        reset_season()
    else:
        api.chat_feed_alert('No Reset')
elif int(data[1]) == 2:
    confirm = e.ccbox('Reset Entire Database?')
    if confirm == True:
        reset_all()
    else:
        api.chat_feed_alert('No Reset')
elif int(data[1]) == 3:
    create_tables()
