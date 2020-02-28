# 2005 minnesota
import csv
import json
import pickle
import pprint

import numpy as np


def get_columns(include_seed_type=True):
    # Open columns
    with open('columns.json', 'r') as column_file:
        columns = json.load(column_file)

    if not include_seed_type:
        columns.remove('SeedType')
    columns.remove('TopScore')
    columns.remove('BotScore')
    columns.remove('TopTOV')
    columns.remove('BotTOV')
    columns.remove('TopTOPer')
    columns.remove('BotTOPer')
    columns.remove('TopTSPer')
    columns.remove('BotTSPer')
    columns.remove('TopFT')
    columns.remove('BotFT')
    columns.remove('TopFTA')
    columns.remove('BotFTA')
    columns.remove('TopFTR')
    columns.remove('BotFTR')
    columns.remove('TopTravel')
    columns.remove('BotTravel')
    columns.remove('TopOppPTS')
    columns.remove('BotOppPTS')

    return columns


if __name__ == '__main__':
    # with open('Models/model.pickle', 'rb') as f:
    #     _, scaler, _ = pickle.load(f)
    #
    # means = scaler.mean_
    # names = get_columns(False)
    # # for i in range(len(means)):
    # #     if names[i][:3] != 'Bot':
    # #         continue
    # #     print(names[i] + ": " + str(means[i]))
    #
    # with open('datafile.csv', 'r') as f:
    #     header = f.readline().strip()
    # line = ''
    # headers = header.split(',')
    # for h in headers:
    #     if h == 'BotSeed':
    #         line += 'Generic Team'
    #     elif h[:3] == 'Bot' and  h in names:
    #         line += str(float(means[names.index(h)]))
    #     line += ','
    # line = line[:-1]
    # with open('generic.csv', 'w') as f:
    #     f.writelines([header + '\n', line])
    # print(header)
    with open('generic.csv', 'r') as f:
        generic_team = f.readlines()[-1].strip().split(',')
    with open('datafile.csv', 'r') as f:
        data_reader = csv.reader(f)
        data_lines = list(data_reader)

    with open('Matchup/matchup.csv', 'w') as f:
        writer = csv.writer(f)

        lines = data_lines[0]

        writer.writerow(lines)
        for line in data_lines[1:]:
            writer.writerow(line[:2] + [0] + line[3:37] + generic_team)
            writer.writerow(line[:2] + [0] + line[3:6] + line[37:] + generic_team)
