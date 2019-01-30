import csv
import os

# from make_datafile import concatenate


def create_matchup_table(team1, team2, year):
    if not os.path.exists('Matchup/'):
        os.makedirs('Matchup')

    with open('datafile.csv', 'r') as datafile:
        matchup_data = []
        with open('Matchup/matchup_data.csv', 'w') as match_file:
            reader = csv.reader(datafile)
            writer = csv.writer(match_file)

            first = True
            teams = [team1, team2]
            for row in reader:
                if (row[6] in teams or row[37] in teams or first) and row[0] != "":
                    # Write rows to data file
                    writer.writerow(row)
                    first = False
                    matchup_data.append(row)

        # Get two highest years for each
        rows = []
        for row in matchup_data:
            if row[6] in teams and (int(row[0])) < rows[0]:
                # TODO: add the two rows that are needed
                pass

        # Write matchup file
        print(matchup_data)
        with open('Matchup/matchup.csv', 'w') as match_file:
            writer = csv.writer(match_file)
        if matchup_data[0][6] in teams and matchup_data[0][37] in teams:
            writer.writerow(matchup_data)
        elif matchup_data[0][6] in teams:
            writer.writerow(matchup_data[0][:37] + matchup_data[1][37:])
        elif matchup_data[0][37] in teams:
            writer.writerow(matchup_data[1][:37] + matchup_data[0][37:])
        print('Matchup Tables Generated')


if __name__ == '__main__':
    create_matchup_table('Villanova', 'Iowa State', 2018)
