import sqlite3
import sys
import csv
from api import api as api


conn = sqlite3.connect('data.db')
cur = conn.cursor()

def upgrade_cost(level):
    try:
        file = csv.DictReader(open('Costs.csv', encoding='utf-8-sig'))
        for row in file:
            x = int(row['Level'])
            if level == x:
                cost = int(row['Cost'])
                return int(cost)
    except:
        pass


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


def upgrade_rushoffense(user):
    stat = get_rushoffense(user) + 1
    offense = int((stat + get_passoffense(user)) / 2)
    cur.execute('UPDATE Season SET rush_offense=? WHERE user=?;',
                (stat, user))
    conn.commit()
    upgrade_overall(user)
    api.bot_chat(f"{user} upgraded their rush offense to level {stat}")
    api.set_metadata('Rush Offense', stat, user)
    api.set_metadata('Offense', offense, user)
    upgrade_offenseoverall(user)


def upgrade_specialteams(user):
    stat = get_specialteams(user) + 1
    cur.execute('UPDATE Season SET special_teams=? WHERE user=?;',
                (stat, user))
    conn.commit()
    api.bot_chat(f"{user} upgraded their special teams to level {stat}")
    upgrade_overall(user)
    api.set_metadata('Special Teams', stat, user)


def upgrade_passoffense(user):
    stat = get_passoffense(user) + 1
    offense = int((stat + get_rushoffense(user)) / 2)
    cur.execute('UPDATE Season SET pass_offense=? WHERE user=?;',
                (stat, user))
    conn.commit()
    upgrade_overall(user)
    api.bot_chat(f"{user} upgraded their pass offense to level {stat}")
    api.set_metadata('Pass Offense', stat, user)
    api.set_metadata('Offense', offense, user)
    upgrade_offenseoverall(user)


def upgrade_passdefense(user):
    stat = get_passdefense(user) + 1
    defense = int((stat + get_rushdefense(user)) / 2)
    cur.execute('UPDATE Season SET pass_defense=? WHERE user=?;',
                (stat, user))
    conn.commit()
    upgrade_overall(user)
    api.bot_chat(f"{user} upgraded their pass defense to level {stat}")
    api.set_metadata('Pass Defense', stat, user)
    api.set_metadata('Defense', defense, user)
    upgrade_defenseoverall(user)


def upgrade_rushdefense(user):
    stat = get_rushdefense(user) + 1
    defense = int((stat + get_passdefense(user)) / 2)
    cur.execute('UPDATE Season SET rush_defense=? WHERE user=?;',
                (stat, user))
    conn.commit()
    upgrade_overall(user)
    api.bot_chat(f"{user} upgraded their rush defense to level {stat}")
    api.set_metadata('Rush Defense', stat, user)
    api.set_metadata('Defense', defense, user)
    upgrade_defenseoverall(user)



try:
    user = sys.argv[1]
    upgrade = int(sys.argv[2])
    if upgrade == 1:
        current_lvl = get_rushoffense(user)
        if current_lvl == 99:
            api.bot_chat(f"{user} you are currently a 99 in rush offense and is the max level.")
        else:
            cost = upgrade_cost(get_rushoffense(user) + 1)
            fcost = "{:,}".format(cost)
            points = int(api.get_currency(user, "Points"))
            if points >= cost:
                upgrade_rushoffense(user)
                api.subtract_currency("Points", cost, user)
            else:
                print("Not Enough Points.")
                api.bot_chat(f"{user} you don't have enough points for that upgrade. You need {fcost} points for that upgrade")
    elif upgrade == 2:
        current_lvl = get_passoffense(user)
        if current_lvl == 99:
            api.bot_chat(f"{user} you are currently a 99 in pass offense and is the max level.")
        else:
            cost = upgrade_cost(get_passoffense(user) + 1)
            points = int(api.get_currency(user, "Points"))
            fcost = "{:,}".format(cost)
            if points >= cost:
                upgrade_passoffense(user)
                api.subtract_currency("Points", cost, user)
            else:
                print("Not Enough Points.")
                api.bot_chat(f"{user} you don't have enough points for that upgrade. You need {fcost} points for that upgrade")
    elif upgrade == 3:
        current_lvl = get_rushdefense(user)
        if current_lvl == 99:
            api.bot_chat(f"{user} you are currently a 99 in pass offense and is the max level.")
        else:
            cost = upgrade_cost(get_rushdefense(user) + 1)
            points = int(api.get_currency(user, "Points"))
            fcost = "{:,}".format(cost)
            if points >= cost:
                upgrade_rushdefense(user)
                api.subtract_currency("Points", cost, user)
            else:
                print("Not Enough Points.")
                api.bot_chat(f"{user} you don't have enough points for that upgrade. You need {fcost} points for that upgrade")
    elif upgrade == 4:
        current_lvl = get_passdefense(user)
        if current_lvl == 99:
            api.bot_chat(f"{user} you are currently a 99 in pass defense and is the max level.")
        else:
            cost = upgrade_cost(get_passdefense(user) + 1)
            points = int(api.get_currency(user, "Points"))
            fcost = "{:,}".format(cost)
            if points >= cost:
                upgrade_passdefense(user)
                api.subtract_currency("Points", cost, user)
            else:
                print("Not Enough Points.")
                api.bot_chat(f"{user} you don't have enough points for that upgrade. You need {fcost} points for that upgrade")
    elif upgrade == 5:
        current_lvl = get_specialteams(user)
        if current_lvl == 99:
            api.bot_chat(f"{user} you are currently a 99 in special teams and is the max level.")
        else:
            cost = upgrade_cost(get_specialteams(user) + 1)
            points = int(api.get_currency(user, "Points"))
            fcost = "{:,}".format(cost)
            if points >= cost:
                upgrade_specialteams(user)
                api.subtract_currency("Points", cost, user)
            else:
                print("Not Enough Points.")
                api.bot_chat(f"{user} you don't have enough points for that upgrade. You need {fcost} points for that upgrade")
except Exception as e:
    api.chat_feed_alert(f'Upgrade Error: {e}')