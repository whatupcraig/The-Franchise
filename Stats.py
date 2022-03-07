import sys
import sqlite3
from api import api as api


conn = sqlite3.connect('data.db')
cur = conn.cursor()


    
def get_min(category):
    cur.execute(f"SELECT * FROM Stats ORDER BY {category} ASC;")
    data = cur.fetchall()
    users = []
    if category == 'yapg':
        message = 'Yards Allowed Per Game'
        for user in data:
            username = user[0]
            yapg = user[4]
            users.append(username)
            users.append(yapg)
    if category == 'papg':
        message = 'Points Allowed Per Game'
        for user in data:
            username = user[0]
            yapg = user[5]
            users.append(username)
            users.append(yapg)
    if category == 'pass_apg':
        message = 'Passing Yards Allowed Per Game'
        for user in data:
            username = user[0]
            yapg = user[9]
            users.append(username)
            users.append(yapg)
    if category == 'rush_apg':
        message = 'Rushing Yards Allowed Per Game'
        for user in data:
            username = user[0]
            yapg = user[10]
            users.append(username)
            users.append(yapg)
    if len(users) <= 2:
        api.bot_chat(f'FRANCHISE STATS: {message}: {users[0]}: {users[1]}')
    elif len(user) <= 4:
        api.bot_chat(f'FRANCHISE STATS: {message}: {users[0]}: {users[1]} | {users[2]}: {users[3]}')
    elif len(user) <= 6:
        api.bot_chat(f'FRANCHISE STATS: {message}: {users[0]}: {users[1]} | {users[2]}: {users[3]} | {users[4]}: {users[5]}')
    elif len(user) <= 8:
        api.bot_chat(f'FRANCHISE STATS: {message}: {users[0]}: {users[1]} | {users[2]}: {users[3]} | {users[4]}: {users[5]} | {users[6]}: {users[7]}')
    else:
        api.bot_chat(f'FRANCHISE STATS: {message}: {users[0]}: {users[1]} | {users[2]}: {users[3]} | {users[4]}: {users[5]} | {users[6]}: {users[7]} | {users[8]}: {users[9]}')


def get_max(category):
    try:
        cur.execute(f"SELECT * FROM Stats ORDER BY {category} DESC;")
        data = cur.fetchall()
        users = []
    except:
        pass
    if category == 'YPG':
        message = 'Top Yards Per Game'
        for user in data:
            username = user[0]
            ypg = user[2]
            users.append(username)
            users.append(ypg)
    if category == 'PPG':
        message = 'Top Points Per Game'
        for user in data:
            username = user[0]
            ppg = user[3]
            users.append(username)
            users.append(ppg)
    if category == 'games':
        message = 'Most Games Played'
        for user in data:
            username = user[0]
            games = user[1]
            users.append(username)
            users.append(games)
    if category == 'pass_ypg':
        message = 'Top Passing Yards Per Game'
        for user in data:
            username = user[0]
            pass_ypg = user[7]
            users.append(username)
            users.append(pass_ypg)
    if category == 'rush_ypg':
        message = 'Top Rushing Yards Per Game'
        for user in data:
            username = user[0]
            rush_ypg = user[8]
            users.append(username)
            users.append(rush_ypg)
    if category == 'sacks':
        message = 'Most Sacks'
        for user in data:
            username = user[0]
            sacks = user[11]
            users.append(username)
            users.append(sacks)
    if category == 'interceptions':
        message = 'Most Interceptions'
        for user in data:
            username = user[0]
            interceptions = user[12]
            users.append(username)
            users.append(interceptions)
    if category == 'fumbles':
        message = 'Most Forced Fumbles'
        for user in data:
            username = user[0]
            fumbles = user[13]
            users.append(username)
            users.append(fumbles)
    if category == 'wins':
        message = 'Most Wins'
        cur.execute(f"SELECT * FROM Season ORDER BY {category} DESC;")
        data = cur.fetchall()
        users = []
        for user in data:
            username = user[0]
            wins = user[10]
            users.append(username)
            users.append(wins)
    try:
        if len(users) <= 2:
            api.bot_chat(f'FRANCHISE STATS: {message}: {users[0]}: {users[1]}')
        elif len(user) <= 4:
            api.bot_chat(f'FRANCHISE STATS: {message}: {users[0]}: {users[1]} | {users[2]}: {users[3]}')
        elif len(user) <= 6:
            api.bot_chat(f'FRANCHISE STATS: {message}: {users[0]}: {users[1]} | {users[2]}: {users[3]} | {users[4]}: {users[5]}')
        elif len(user) <= 8:
            api.bot_chat(f'FRANCHISE STATS: {message}: {users[0]}: {users[1]} | {users[2]}: {users[3]} | {users[4]}: {users[5]} | {users[6]}: {users[7]}')
        else:
            api.bot_chat(f'FRANCHISE STATS: {message}: {users[0]}: {users[1]} | {users[2]}: {users[3]} | {users[4]}: {users[5]} | {users[6]}: {users[7]} | {users[8]}: {users[9]}')
    except Exception as e:
        api.chat_feed_alert(f'Failed to get stats: {e}')


def get_userstats(user):
    cur.execute("SELECT * FROM Stats WHERE user=?", (user,))
    data = cur.fetchall()[0]
    games = data[1]
    ypg = data[2]
    ppg = data[3]
    yapg = data[4]
    papg = data[5]
    pass_ypg = data[7]
    rush_ypg = data[8]
    pass_apg = data[9]
    rush_apg = data[10]
    sacks = data[11]
    interceptions = data[12]
    fumbles = data[13]
    cur.execute("SELECT * FROM Season WHERE user=?", (user,))
    season = cur.fetchall()[0]
    wins = season[10]
    losses = season[11]
    ties = season[12]
    api.bot_chat(f"FRANCHISE SEASON STATS: {user}: Games: {games} | Record: {wins} - {losses} - {ties} | Yards Per Game: {ypg} | Points Per Game: {ppg} | Yards Allowed Per Game: {yapg} | Points Allowed Per Game: {papg} | Pass Yards Per Game: {pass_ypg} | Rush Yards Per Game: {rush_ypg} | Passing Yards Allowed Per Game: {pass_apg} | Rushing Yards Allowed Per Game: {rush_apg} | Sacks: {sacks} | Interceptions: {interceptions} | Fumbles: {fumbles}")


data_list = 'YPG', 'PPG', 'games', 'sacks', 'interceptions', 'pass_ypg', 'rush_ypg', 'fumbles', 'wins'
min_list = 'yapg', 'papg', 'pass_apg', 'rush_apg'
data = sys.argv[1]
if data in data_list:
    get_max(data)
elif data in min_list:
    get_min(data)
else:
    get_userstats(data)