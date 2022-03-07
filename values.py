import csv

with open('Values.csv', 'r', encoding='utf-8-sig') as file:
    csvreader = csv.reader(file)

    data = []
    for row in csvreader:
        data.append(row)


sleep_quarter = int(data[18][1])
sleep_per_play = float(data[0][1])

#Run Play Modifiers
run_big_play_success = float(data[1][1])
run_med_play_success = float(data[2][1])
run_reg_play_success = float(data[3][1])

#Pass Play Modifers
pass_big_play_success = int(data[4][1])
pass_med_play_success = int(data[5][1])
pass_regular_play_success = int(data[6][1])

#Momentum
turnover_momentum = int(data[7][1])

#Bonus Multipler for chance
bonus_multipler = float(data[8][1])

#Difference Multipler for chance
difference_multipler = float(data[9][1])

#Win Loss Reward
win_reward = int(data[10][1])
loss_reward = int(data[11][1])

#Bonus Rewards
five_win_bonus = int(data[12][1])
ten_win_bonus = int(data[13][1])
twenty_win_bonus = int(data[14][1])
thirty_win_bonus = int(data[15][1])
fifty_win_bonus = int(data[16][1])