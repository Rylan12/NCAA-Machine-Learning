"""
Written by Kevin Nowland and Matthew Osborne
Last Updated on Feb 16, 2018

Using sports-reference.com to create .csv files with data for first round
games in a given year"s tournament.
"""

# Import thee packages we will need
import bs4
import requests
import logging

# Set up the log
logging.basicConfig(level=logging.INFO)


def get_team_stats(team_url):
    """
    This function takes in a teams's url and scrapes the html file for the 
    desired statistics. Spits out -9999 for stats that are missing."""

    logging.info('get_team_stats: entered')
    logging.info('get_team_stats: get response from ' + team_url)
    response = requests.get(team_url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # Initialize the dictionary
    stats = {
        'games': 0,
        'fg': 0,
        'fga': 0,
        'fgPerc': 0.0,
        '3p': 0,
        '3pa': 0,
        '3pPerc': 0.0,
        '2p': 0,
        '2pa': 0,
        '2pPerc': 0.0,
        'ft': 0,
        'fta': 0,
        'ftPerc': 0.0,
        'drb': 0,
        'orb': 0,
        'ast': 0,
        'stl': 0,
        'blk': 0,
        'tov': 0,
        'pts': 0,
        'opp_pts': 0,
        'poss': 0,
        'tsPerc': 0.0,
        'efgPerc': 0.0,
        'toPerc': 0.0,
        'ftr': 0.0,
        'ortg': 0.0,
        'drtg': 0.0,
        'sos': 0.0
    }

    # read off values from sports-ref table
    logging.info('get_team_stats: getting stats from the soup')
    tr_stats = soup.find('table', id='team_stats').find_all('tr')[1]
    stats['games'] = int('0' + tr_stats.find('td', {'data-stat': 'g'}).text)
    stats['fg'] = int('0' + tr_stats.find('td', {"data-stat": 'fg'}).text)
    stats['fga'] = int('0' + tr_stats.find('td', {"data-stat": 'fga'}).text)
    stats['fgPerc'] = float(
        '0' + tr_stats.find('td', {"data-stat": "fg_pct"}).text)
    stats['3p'] = int('0' + tr_stats.find('td', {"data-stat": 'fg3'}).text)
    stats['3pa'] = int('0' + tr_stats.find('td', {"data-stat": 'fg3a'}).text)
    stats['3pPerc'] = float(
        '0' + tr_stats.find('td', {"data-stat": "fg3_pct"}).text)
    stats['2p'] = int('0' + tr_stats.find('td', {"data-stat": 'fg2'}).text)
    stats['2pa'] = int('0' + tr_stats.find('td', {"data-stat": 'fg2a'}).text)
    stats['2pPerc'] = float(
        '0' + tr_stats.find('td', {"data-stat": "fg_pct"}).text)
    stats['ft'] = int('0' + tr_stats.find('td', {"data-stat": 'ft'}).text)
    stats['fta'] = int('0' + tr_stats.find('td', {"data-stat": 'fta'}).text)
    stats['ftPerc'] = float(
        '0' + tr_stats.find('td', {"data-stat": "ft_pct"}).text)
    stats['drb'] = int('0' + tr_stats.find('td', {"data-stat": 'drb'}).text)
    stats['orb'] = int('0' + tr_stats.find('td', {"data-stat": 'orb'}).text)
    stats['ast'] = int('0' + tr_stats.find('td', {"data-stat": 'ast'}).text)
    stats['stl'] = int('0' + tr_stats.find('td', {"data-stat": 'stl'}).text)
    stats['blk'] = int('0' + tr_stats.find('td', {"data-stat": 'blk'}).text)
    stats['tov'] = int('0' + tr_stats.find('td', {"data-stat": 'tov'}).text)
    stats['pts'] = int('0' + tr_stats.find('td', {"data-stat": 'pts'}).text)

    tr_opp_stats = soup.find('table', id="team_stats").find_all('tr')[3]
    stats["opp_pts"] = \
        int('0' + tr_opp_stats.find('td', {"data-stat": "opp_pts"}).text)

    # If the stat is 0 it is missing, we recode it as -9999
    for i in stats:
        if stats[i] == 0:
            stats[i] = -9999

    logging.info("get_team_stats: calculating advanced stats")
    # calculate 'advanced' stats
    # can"t get orb% because don"t have opponent defensive rebounds
    # For each advanced stat we check if the needed traditional stat is missing, then 
    # code accordingly.
    if (stats['orb'] == -9999 or stats['drb'] == -9999 or stats['fga'] == -9999
            or stats['fta'] == -9999 or stats['tov'] == -9999 or stats[
                'fg'] == -9999):
        stats['poss'] = -9999
        stats['toPerc'] = -9999
        stats['ortg'] = -9999
        stats['drtg'] = -9999
    else:
        stats['poss'] = 0.5 * ((stats['fga'] + 0.4 * stats['fta'] - 1.07 *
                                (stats['orb'] / (
                                            stats['drb'] + stats['orb'])) *
                                (stats['fga'] - stats['fg']) + stats['tov']) +
                               (stats['fga'] + 0.4 * stats['fta'] - 1.07 *
                                (stats['orb'] / (
                                            stats['drb'] + stats['orb'])) *
                                (stats['fga'] - stats['fg']) + stats['tov']))
        stats['toPerc'] = stats['tov'] / stats['poss']

    # calculate ortg if possible    
    if stats['pts'] == -9999 or stats['poss'] == -9999:
        stats['ortg'] = -9999
    else:
        stats['ortg'] = stats['pts'] / stats['poss']

    # calculate drtg if possible
    if stats["opp_pts"] == -9999 or stats['poss'] == -9999:
        stats['drtg'] = -9999
    else:
        stats['drtg'] = stats["opp_pts"] / stats['poss']

    # calculate tsPerc if possible    
    if stats['pts'] == -9999 or stats['fga'] == -9999 or stats['fta'] == -9999:
        stats['tsPerc'] = -9999
    else:
        stats['tsPerc'] = stats['pts'] / (
                    2 * (stats['fga'] + 0.44 * stats['fta']))

    # calculate efgPerc if possible
    if stats['fga'] == -9999 or stats['3p'] == -9999 or stats['fg'] == -9999:
        stats['efgPerc'] = -9999
    else:
        stats['efgPerc'] = (0.5 * stats['3p'] + stats['fg']) / stats['fga']

    # calculate ftr if possible
    if stats['fta'] == -9999 or stats['fga'] == -9999:
        stats['ftr'] = -9999
    else:
        stats['ftr'] = stats['fta'] / stats['fga']

    # get strength of schedule
    logging.info("get_team_stats: getting strength of schedule")
    div_meta = soup.find('div', id='meta')
    # sos_text = ""
    for p in div_meta.find_all('p'):
        if p.strong is not None:
            if p.strong.text == "SOS:":
                stats['sos'] = float(p.text.split()[1])
                break

    logging.info("get_team_stats: exiting")
    return stats


def write_team_stats(f, stats, current=False):
    """writes the team stats in order in the file"""

    logging.info('write_team_stats: entered')
    f.write(str(stats['games']).strip() + ',')
    f.write(str(stats['fg']).strip() + ',')
    f.write(str(stats['fga']).strip() + ',')
    f.write(str(stats['fgPerc']).strip() + ',')
    f.write(str(stats['3p']).strip() + ',')
    f.write(str(stats['3pa']).strip() + ',')
    f.write(str(stats['3pPerc']).strip() + ',')
    f.write(str(stats['2p']).strip() + ',')
    f.write(str(stats['2pa']).strip() + ',')
    f.write(str(stats['2pPerc']).strip() + ',')
    f.write(str(stats['pts']).strip() + ',')
    f.write(str(stats['opp_pts']).strip() + ',')
    f.write(str(stats['ast']).strip() + ',')
    f.write(str(stats['orb']).strip() + ',')
    f.write(str(stats['drb']).strip() + ',')
    f.write(str(stats['poss']).strip() + ',')
    f.write(str(stats['tsPerc']).strip() + ',')
    f.write(str(stats['efgPerc']).strip() + ',')
    f.write(str(stats['tov']).strip() + ',')
    f.write(str(stats['toPerc']).strip() + ',')
    f.write(str(stats['ft']).strip() + ',')
    f.write(str(stats['fta']).strip() + ',')
    f.write(str(stats['ftr']).strip() + ',')
    f.write(str(stats['ortg']).strip() + ',')
    f.write(str(stats['drtg']).strip() + ',')
    f.write(str(stats['sos']).strip() + ',' if not current else '')
    logging.info('write_team_stats: exiting')


def make_yearfile(year, current=False):
    """makes file for a single year
    This code will only work for the years 2001-2018"""

    # Check to make sure year is in range 2001-2017
    if int(year) < 2001:
        print('Sorry our code only works for the years 2001-2018')
        return

    logging.info('make_yearfile: entered')
    file_name = 'Data Files/ncaa' + str(
        year) + "EDIT.csv" if not current else 'current.csv'

    lines = []
    try:
        with open(file_name, 'r') as f:
            lines = f.readlines()
        backup = True
    except FileNotFoundError:
        backup = False

    try:
        with open(file_name, 'w') as f:
            logging.info('make_yearfile: writing to: ' + file_name)
            f.write(
                'Region,GameCity,GameState,seed,team,score,games,fg,fga,fgPerc,3p,3pa,'
                '3pPerc,2p,2pa,2pPerc,pts,opp_pts,ast,orb,drb,poss,tsPerc,efgPerc,tov,'
                'toPerc,ft,fta,ftr,ortg,drtg,sos' + (
                    ',loss' if not current else '') + '\n')
            get_game_info(f)

        # Done writing data to file
        logging.info('make_yearfile: exiting')
    # Backup
    except IndexError:
        if backup:
            with open(file_name, 'w') as f:
                f.writelines(lines)


def get_game_info(f):
    # logging.info('make_yearfile: %s', link[1])
    links = [[16, 'North Carolina Central', 'https://www.sports-reference.com/cbb/schools/north-carolina-central/2019.html'],
             [16, 'North Dakota State', 'https://www.sports-reference.com/cbb/schools/north-dakota-state/2019.html'],
             [11, 'Temple', 'https://www.sports-reference.com/cbb/schools/temple/2019.html'],
             [11, 'Belmont', 'https://www.sports-reference.com/cbb/schools/belmont/2019.html'],
             [16, 'Prairie View', 'https://www.sports-reference.com/cbb/schools/prairie-view/2019.html'],
             [16, 'Fairleigh Dickinson', 'https://www.sports-reference.com/cbb/schools/fairleigh-dickinson/2019.html'],
             [11, "St. John's (NY)", 'https://www.sports-reference.com/cbb/schools/st-johns-ny/2019.html'],
             [11, 'Arizona State', 'https://www.sports-reference.com/cbb/schools/arizona-state/2019.html']]
    # Higher seed data first
    for link in links:
        f.write('FILL IN,')  # Bracket Region
        f.write('TBD,')  # game location
        f.write('TBD,')  # game location
        f.write(str(link[0]) + ',')  # higher seed
        f.write(link[1] + ',')  # name
        f.write(',')  # score
        team_url = link[2]
        logging.info('make_yearfile: getting response from: ' + team_url)
        stats = get_team_stats(team_url)
        write_team_stats(f, stats)
        f.write('\n')

# Uncomment the below lines to write csv files for all years 2001-2017
if __name__ == '__main__':
    # make_yearfile(2019)
    make_yearfile(2019)
