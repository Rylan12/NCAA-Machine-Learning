import csv
from os import listdir
from make_yearfiles import make_yearfile
from seed_type import SeedType

COLUMNS = [
    'year',
    'SeedType',
    'Upset',
    'Region',
    'GameCity',
    'GameState',
    'TopSeed',
    'TopCity',
    'TopST',
    'TopTravel',
    'TopScore',
    'TopGames',
    'TopFG',
    'TopFGA',
    'TopFGPer',
    'Top3P',
    'Top3PA',
    'Top3Per',
    'Top2P',
    'Top2PA',
    'Top2Per',
    'TopPTs',
    'TopOppPTS',
    'TopAST',
    'TopORB',
    'TopDRB',
    'TopPoss',
    'TopTSPer',
    'TopEFGPer',
    'TopTOV',
    'TopTOPer',
    'TopFT',
    'TopFTA',
    'TopFTR',
    'TopORTG',
    'TopDRTG',
    'TopSOS',
    'BotSeed',
    'BotCity',
    'BotST',
    'BotTravel',
    'BotScore',
    'BotGames',
    'BotFG',
    'BotFGA',
    'BotFGPer',
    'Bot3P',
    'Bot3PA',
    'Bot3Per',
    'Bot2P',
    'Bot2PA',
    'Bot2Per',
    'BotPTs',
    'BotOppPTS',
    'BotAST',
    'BotORB',
    'BotDRB',
    'BotPoss',
    'BotTSPer',
    'BotEFGPer',
    'BotTOV',
    'BotTOPer',
    'BotFT',
    'BotFTA',
    'BotFTR',
    'BotORTG',
    'BotDRTG',
    'BotSOS',
]


def get_year(file):
    return file[-8:-4]


def concatenate(directory):
    # Get all year files
    years = []
    for year in listdir(directory):
        if year != '.DS_Store':
            years.append(directory + '/' + year)

    # Extract data from year files
    data = {}
    for year in years:
        data[int(get_year(year))] = get_data_file(year)

    # Set up data file
    datafile = []

    # Fill main datafile
    for year in range(min(data), max(data) + 1):
        for row in range(0, len(data[year]), 2):
            # Two rows at a time
            year_lines = [data[year][row], data[year][row + 1]]

            # Set up line
            line = [None for _ in range(68)]
            # year, SeedType, Upset
            line[:3] = [year, SeedType({year_lines[0][3], year_lines[1][3]}).name, year_lines[0][32]]
            # Region, GameCity, GameState
            line[3:6] = year_lines[0][0:3]

            # Insert values
            for slot in range(len(year_lines)):
                # Index modifier value
                mod = slot * 31

                # Seed, City, ST, Travel
                line[mod + 6:mod + 10] = [year_lines[slot][4], '', '', '']  # Implement: City, ST, Travel
                # Score, Games, FG, FGA, FGPer, 3P, 3PA, 3Per, 2P, 2PA, 2Per, PTs, OppPTS, AST,
                #   ORB, DRB, Poss, TSPer, EFGPer, TOV, TOPer, FT, FTA, FTR, ORTG, DRTG, SOS
                line[mod + 10:mod + 37] = year_lines[slot][5:32]

            # Write new line to file
            datafile.append(line)

    # Sort datafile
    datafile = sorted(datafile, key=lambda x: SeedType.get_type_index(x[1]))
    datafile = sorted(datafile, key=lambda x: x[0])

    # Insert headers
    datafile.insert(0, COLUMNS)

    # Write data
    with open('datafile.csv', 'w') as file:
        writer = csv.writer(file)
        for line in datafile:
            writer.writerow(line)


def get_data_file(yearfile):
    data = []
    with open(yearfile, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data[1:]


if __name__ == '__main__':
    current_year = 2019

    # Collect all necessary data files (only if needed)
    for i in range(2001, current_year):
        if 'ncaa' + str(i) + '.csv' not in listdir('Data Files'):
            make_yearfile(i)

    # Concatenate into single data file
    concatenate('Data Files')

    make_yearfile(current_year, True)
