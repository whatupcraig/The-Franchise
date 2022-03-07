from lzma import PRESET_DEFAULT
import sqlite3
import sys
from functions import get_bet, log
from api import api as api
import time



users = sys.argv
player_one = users[1]
player_two = users[2]
api.bot_chat(f"FRANCHISE CHALLENGE: @{player_two} {player_one} challenged you! Use !accept to accept the challenge.")
wait = 60
while wait > 0:
    status = api.get_variable(f'challenge{player_two}')
    time.sleep(5)
    wait -= 5
    if status == "Accept":
        api.customvariable(f'challenge{player_two}', 'null', 30)
        api.add_role('Challenge',player_one)
        api.add_role('Challenge',player_two)
        api.bot_chat('FRANCHISE CHALLENGE: Did you want to place a wager? Use !franchise <number> to place a bet. EXAMPLE: !franchise 500')
        wait = 30
        player_onebet = int(api.get_variable(f'wager{player_one}'))
        player_twobet = int(api.get_variable(f'wager{player_two}'))
        while wait > 0:
            if player_onebet or player_twobet > 0:
                if player_onebet <= player_twobet:
                    wager = player_onebet
                    api.bot_chat(f'FRANCHISE CHALLENGE: {player_one} suggessted a wager of {"{:,}".format(wager)} points. {player_two} use !accept to accept the bet')
                    wait = 30
                    while wait > 0:
                        status = api.get_variable(f'challenge{player_two}')
                        if status == 'Accept':
                            wager = player_onebet
                            break
                        wait -= 5
                        time.sleep(5)
                        if wait <= 0:
                            api.bot_chat(f'{player_two} did not respond in time. There is no wager')
                            break
                else:
                    wager = player_twobet
                    api.bot_chat(f'FRANCHISE CHALLENGE: {player_two} suggessted a wager of {"{:,}".format(wager)} points. {player_one} use !accept to accept the bet')
                    wait = 30
                    while wait > 0:
                        status = api.get_variable(f'challenge{player_two}')
                        if status == 'Accept':
                            wager = player_twobet
                            break
                        wait -= 5
                        time.sleep(5)
                        if wait <= 0:
                            api.bot_chat(f'{player_two} did not respond in time. There is no wager')
                            break
                break
            wait -= 5
            time.sleep(5)
            if wait <= 0:
                api.bot_chat("FRANCHISE CHALLENGE: No wager was suggessted")
                wager = 0
                break
        api.preset_effect('Start Football Game', arg='Player One', argdata=player_one, arg2='Player Two', arg2data=player_two)
        api.customvariable(f'challenge{player_two}', 'null', 30)
        api.customvariable(f'challenge{player_one}', 'null', 30)
    if wait < 0:
        api.bot_chat(f'{player_two} did not respond in time')
        break