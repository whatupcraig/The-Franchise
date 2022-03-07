from logging import exception
import sqlite3
import sys
import csv
from api import api as api


conn = sqlite3.connect('data.db')
cur = conn.cursor()


def upgrade_overall(user):
    rush_o = get_rushoffense(user)
    pass_o = get_passoffense(user)
    rush_d = get_rushdefense(user)
    pass_d = get_passdefense(user)
    special_teams = get_specialteams(user)
    overall = int((rush_o + pass_o + rush_d + pass_d + special_teams) / 5)
    cur.execute('UPDATE Season SET overall=? WHERE user=?;',
                (overall, user))
    conn.commit()
    api.set_metadata('Overall', overall, user)


def upgrade_offenseoverall(user):
    rush_o = get_rushoffense(user)
    pass_o = get_passoffense(user)
    overall = int((rush_o + pass_o) / 2)
    cur.execute('UPDATE Season SET offense=? WHERE user=?;',
                (overall, user))
    conn.commit()
    api.set_metadata('Offense', overall, user)


def upgrade_defenseoverall(user):
    rush_d = get_rushdefense(user)
    pass_d = get_passdefense(user)
    overall = int((rush_d + pass_d) / 2)
    cur.execute('UPDATE Season SET defense=? WHERE user=?;',
                (overall, user))
    conn.commit()
    api.set_metadata('Defense', overall, user)


def get_rushoffense(user):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Season WHERE user=?", (user,))
    data = cur.fetchall()
    offense = data[0][4]
    return int(offense)


def get_passoffense(user):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Season WHERE user=?", (user,))
    data = cur.fetchall()
    offense = data[0][5]
    return int(offense)


def get_passdefense(user):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Season WHERE user=?", (user,))
    data = cur.fetchall()
    offense = data[0][7]
    return int(offense)


def get_rushdefense(user):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Season WHERE user=?", (user,))
    data = cur.fetchall()
    defense = data[0][6]
    return int(defense)


def get_specialteams(user):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Season WHERE user=?", (user,))
    data = cur.fetchall()
    defense = data[0][8]
    return int(defense)


def get_offense(user):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Season WHERE user=?", (user,))
    data = cur.fetchall()
    offense = data[0][2]
    return int(offense)


def get_defense(user):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Season WHERE user=?", (user,))
    data = cur.fetchall()
    defense = data[0][3]
    return int(defense)


def upgrade_rushoffense(user, amount):
    offense = int((amount + get_passoffense(user)) / 2)
    cur.execute('UPDATE Season SET rush_offense=? WHERE user=?;',
                (amount, user))
    cur.execute('UPDATE Season SET offense=? WHERE user=?;',
                (offense, user))
    conn.commit()
    upgrade_overall(user)
    api.bot_chat(f"{user} upgraded their rush offense to level {amount}")
    api.set_metadata('Rush Offense', amount, user)
    upgrade_offenseoverall(user)


def upgrade_specialteams(user, amount):
    cur.execute('UPDATE Season SET special_teams=? WHERE user=?;',
                (amount, user))
    conn.commit()
    upgrade_overall(user)
    api.bot_chat(f"{user} upgraded their special teams to level {amount}")
    api.set_metadata('Special Teams', amount, user)


def upgrade_passoffense(user, amount):
    offense = int((amount + get_rushoffense(user)) / 2)
    cur.execute('UPDATE Season SET pass_offense=? WHERE user=?;',
                (amount, user))
    cur.execute('UPDATE Season SET offense=? WHERE user=?;',
                (offense, user))
    conn.commit()
    upgrade_overall(user)
    api.bot_chat(f"{user} upgraded their pass offense to level {amount}")
    api.set_metadata('Pass Offense', amount, user)
    upgrade_offenseoverall(user)


def upgrade_passdefense(user, amount):
    defense = int((amount + get_rushdefense(user)) / 2)
    cur.execute('UPDATE Season SET pass_defense=? WHERE user=?;',
                (amount, user))
    cur.execute('UPDATE Season SET defense=? WHERE user=?;',
                (defense, user))
    conn.commit()
    upgrade_overall(user)
    api.bot_chat(f"{user} upgraded their pass defense to level {amount}")
    api.set_metadata('Pass Defense', amount, user)
    upgrade_defenseoverall(user)


def upgrade_rushdefense(user, amount):
    defense = int((amount + get_passdefense(user)) / 2)
    cur.execute('UPDATE Season SET rush_defense=? WHERE user=?;',
                (amount, user))
    cur.execute('UPDATE Season SET defense=? WHERE user=?;',
                (defense, user))
    conn.commit()
    upgrade_overall(user)
    api.bot_chat(f"{user} upgraded their rush defense to level {amount}")
    api.set_metadata('Rush Defense', amount, user)
    upgrade_defenseoverall(user)


try:
    user = sys.argv[1]
    upgrade = int(sys.argv[2])
    amount = int(sys.argv[3])

    if upgrade == 1:
        upgrade_rushoffense(user, amount)
    elif upgrade == 2:
        upgrade_passoffense(user, amount)
    elif upgrade == 3:
        upgrade_rushdefense(user, amount)
    elif upgrade == 4:
        upgrade_passdefense(user, amount)
    elif upgrade == 5:
        upgrade_specialteams(user, amount)
except Exception as e:
    api.chat_feed_alert(f'Error upgrading {user} Team: {e}')