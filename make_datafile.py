# noinspection SpellCheckingInspection
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

    logging.info("get_team_stats: entered")
    logging.info("get_team_stats: get response from" + team_url)
    response = requests.get(team_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # Initialize the dictionary
    stats = {
        "games": 0,
        "fg": 0,
        "fga": 0,
        "fgPerc": 0.0,
        "3p": 0,
        "3pa": 0,
        "3pPerc": 0.0,
        "2p": 0,
        "2pa": 0,
        "2pPerc": 0.0,
        "ft": 0,
        "fta": 0,
        "ftPerc": 0.0,
        "drb": 0,
        "orb": 0,
        "ast": 0,
        "stl": 0,
        "blk": 0,
        "tov": 0,
        "pts": 0,
        "opp_pts": 0,
        "poss": 0,
        "tsPerc": 0.0,
        "efgPerc": 0.0,
        "toPerc": 0.0,
        "ftr": 0.0,
        "ortg": 0.0,
        "drtg": 0.0,
        "sos": 0.0
    }

    # read off values from sports-ref table
    logging.info("get_team_stats: getting stats from the soup")
    tr_stats = soup.find("table", id="team_stats").find_all("tr")[1]
    stats["games"] = int("0" + tr_stats.find("td", {"data-stat": "g"}).text)
    stats["fg"] = int("0" + tr_stats.find("td", {"data-stat": "fg"}).text)
    stats["fga"] = int("0" + tr_stats.find("td", {"data-stat": "fga"}).text)
    stats["fgPerc"] = float("0" + tr_stats.find("td", {"data-stat": "fg_pct"}).text)
    stats["3p"] = int("0" + tr_stats.find("td", {"data-stat": "fg3"}).text)
    stats["3pa"] = int("0" + tr_stats.find("td", {"data-stat": "fg3a"}).text)
    stats["3pPerc"] = float("0" + tr_stats.find("td", {"data-stat": "fg3_pct"}).text)
    stats["2p"] = int("0" + tr_stats.find("td", {"data-stat": "fg2"}).text)
    stats["2pa"] = int("0" + tr_stats.find("td", {"data-stat": "fg2a"}).text)
    stats["2pPerc"] = float("0" + tr_stats.find("td", {"data-stat": "fg_pct"}).text)
    stats["ft"] = int("0" + tr_stats.find("td", {"data-stat": "ft"}).text)
    stats["fta"] = int("0" + tr_stats.find("td", {"data-stat": "fta"}).text)
    stats["ftPerc"] = float("0" + tr_stats.find("td", {"data-stat": "ft_pct"}).text)
    stats["drb"] = int('0' + tr_stats.find("td", {"data-stat": "drb"}).text)
    stats["orb"] = int('0' + tr_stats.find("td", {"data-stat": "orb"}).text)
    stats["ast"] = int("0" + tr_stats.find("td", {"data-stat": "ast"}).text)
    stats["stl"] = int("0" + tr_stats.find("td", {"data-stat": "stl"}).text)
    stats["blk"] = int("0" + tr_stats.find("td", {"data-stat": "blk"}).text)
    stats["tov"] = int("0" + tr_stats.find("td", {"data-stat": "tov"}).text)
    stats["pts"] = int("0" + tr_stats.find("td", {"data-stat": "pts"}).text)

    tr_opp_stats = soup.find("table", id="team_stats").find_all("tr")[3]
    stats["opp_pts"] = \
        int("0" + tr_opp_stats.find("td", {"data-stat": "opp_pts"}).text)

    # If the stat is 0 it is missing, we recode it as -9999
    for i in stats:
        if stats[i] == 0:
            stats[i] = -9999

    logging.info("get_team_stats: calculating advanced stats")
    # calculate "advanced" stats
    # can"t get orb% because don"t have opponent defensive rebounds
    # For each advanced stat we check if the needed traditional stat is missing, then 
    # code accordingly.
    if (stats["orb"] == -9999 or stats["drb"] == -9999 or stats["fga"] == -9999
            or stats["fta"] == -9999 or stats["tov"] == -9999 or stats["fg"] == -9999):
        stats["poss"] = -9999
        stats["toPerc"] = -9999
        stats["ortg"] = -9999
        stats["drtg"] = -9999
    else:
        stats["poss"] = 0.5 * ((stats["fga"] + 0.4 * stats["fta"] - 1.07 *
                                (stats["orb"] / (stats["drb"] + stats["orb"])) *
                                (stats["fga"] - stats["fg"]) + stats["tov"]) +
                               (stats["fga"] + 0.4 * stats["fta"] - 1.07 *
                                (stats["orb"] / (stats["drb"] + stats["orb"])) *
                                (stats["fga"] - stats["fg"]) + stats["tov"]))
        stats["toPerc"] = stats["tov"] / stats["poss"]

    # calculate ortg if possible    
    if stats["pts"] == -9999 or stats["poss"] == -9999:
        stats["ortg"] = -9999
    else:
        stats["ortg"] = stats["pts"] / stats["poss"]

    # calculate drtg if possible
    if stats["opp_pts"] == -9999 or stats["poss"] == -9999:
        stats["drtg"] = -9999
    else:
        stats["drtg"] = stats["opp_pts"] / stats["poss"]

    # calculate tsPerc if possible    
    if stats["pts"] == -9999 or stats["fga"] == -9999 or stats["fta"] == -9999:
        stats["tsPerc"] = -9999
    else:
        stats["tsPerc"] = stats["pts"] / (2 * (stats["fga"] + 0.44 * stats["fta"]))

    # calculate efgPerc if possible
    if stats["fga"] == -9999 or stats["3p"] == -9999 or stats["fg"] == -9999:
        stats["efgPerc"] = -9999
    else:
        stats["efgPerc"] = (0.5 * stats["3p"] + stats["fg"]) / stats["fga"]

    # calculate ftr if possible
    if stats["fta"] == -9999 or stats["fga"] == -9999:
        stats["ftr"] = -9999
    else:
        stats["ftr"] = stats["fta"] / stats["fga"]

    # get strength of schedule
    logging.info("get_team_stats: getting strength of schedule")
    div_meta = soup.find("div", id="meta")
    # sos_text = ""
    for p in div_meta.find_all("p"):
        if p.strong is not None:
            if p.strong.text == "SOS:":
                stats["sos"] = float(p.text.split()[1])
                break

    logging.info("get_team_stats: exiting")
    return stats


def write_team_stats(f, stats):
    """writes the team stats in order in the file"""

    logging.info("write_team_stats: entered")
    f.write(str(stats["games"]) + ",")
    f.write(str(stats["fg"]) + ",")
    f.write(str(stats["fga"]) + ",")
    f.write(str(stats["fgPerc"]) + ",")
    f.write(str(stats["3p"]) + ",")
    f.write(str(stats["3pa"]) + ",")
    f.write(str(stats["3pPerc"]) + ",")
    f.write(str(stats["2p"]) + ",")
    f.write(str(stats["2pa"]) + ",")
    f.write(str(stats["2pPerc"]) + ",")
    f.write(str(stats["pts"]) + ",")
    f.write(str(stats["opp_pts"]) + ",")
    f.write(str(stats["ast"]) + ",")
    f.write(str(stats["orb"]) + ",")
    f.write(str(stats["drb"]) + ",")
    f.write(str(stats["poss"]) + ",")
    f.write(str(stats["tsPerc"]) + ",")
    f.write(str(stats["efgPerc"]) + ",")
    f.write(str(stats["tov"]) + ",")
    f.write(str(stats["toPerc"]) + ",")
    f.write(str(stats["ft"]) + ",")
    f.write(str(stats["fta"]) + ",")
    f.write(str(stats["ftr"]) + ",")
    f.write(str(stats["ortg"]) + ",")
    f.write(str(stats["drtg"]) + ",")
    f.write(str(stats["sos"]))
    logging.info("write_team_stats: exiting")


def make_yearfile(year):
    """makes file for a single year"""
    """This code will only work for the years 2001-2017"""

    # Check to make sure year is in range 2001-2017
    if int(year) < 2001:
        print("Sorry our code only works for the years 2001-2017")
        return

    logging.info("make_yearfile: entered")
    file_name = "ncaa" + str(year) + ".csv"
    f = open(file_name, "w")
    logging.info("make_yearfile: writing to: " + file_name)
    f.write("Region,GameCity,GameState,seed,team,score,games,fg,fga,fgPerc,3p,3pa,\
            3pPerc,2p,2pa,2pPerc,pts,opp_pts,ast,orb,drb,poss,tsPerc,efgPerc,tov,\
            toPerc,ft,fta,ftr,ortg,drtg,sos\n")

    # load the web page
    sports_ref_url = "https://www.sports-reference.com"
    year_url = sports_ref_url + "/cbb/postseason/" + str(year) + "-ncaa.html"
    logging.info("make_yearfile: getting response from " + year_url)
    response = requests.get(year_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # the page is organized by round
    # The bracket is broken into four regions, some years have different regions than
    # others. Here we break up the code depending on the year entered.
    if year == 2004:
        # These are the four regions for 2004
        stl = soup.find_all("div", {"id": "stlouis"})
        atl = soup.find_all("div", {"id": "atlanta"})
        erf = soup.find_all("div", {"id": "eastrutherford"})
        phx = soup.find_all("div", {"id": "phoenix"})

        # Get data for all teams in st louis region
        rounds = stl[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            logging.info("make_yearfile: %s", links[0].text)
            # Higher seed data first
            f.write("One,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower seed data second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("One,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

        # Get data for all teams in atlanta region
        rounds = atl[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            logging.info("make_yearfile: %s", links[0].text)
            # Higher Seed first
            f.write("Two,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower Seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Two,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

            # Get data for all teams in eastrutherford region
        rounds = erf[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher Seed First
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Three,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower Seed Second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Three,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

            # Get data for all teams in phoenix region
        rounds = phx[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher Seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Four,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Four,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

    elif year == 2005:
        # In 2005 the regions were syracuse, albuquerque, austin, chicago
        syr = soup.find_all("div", {"id": "syracuse"})
        abq = soup.find_all("div", {"id": "albuquerque"})
        aus = soup.find_all("div", {"id": "austin"})
        chi = soup.find_all("div", {"id": "chicago"})

        # Get data for syracuse region
        rounds = syr[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("One,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("One,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

        # Get data for all teams in albuquerque region
        rounds = abq[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher Seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Two,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Two,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

            # Get data for all teams in austin region
        rounds = aus[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Three,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower Seed Second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Three,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

            # Get data for all teams in chicago region
        rounds = chi[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Four,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Four,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

    elif year == 2006:
        #  Regions in 2006 are minneapolis, atlanta, oakland, washington
        minn = soup.find_all("div", {"id": "minneapolis"})
        atl = soup.find_all("div", {"id": "atlanta"})
        oak = soup.find_all("div", {"id": "oakland"})
        wsh = soup.find_all("div", {"id": "washington"})

        # Get data for all teams in minneapolis region
        rounds = minn[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("One,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("One,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

        # Get data for all teams in atlanta region
        rounds = atl[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Two,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Two,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

            # Get data for all teams in oakland region
        rounds = oak[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Three,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Three,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

        # Get data for all teams in washington region
        rounds = wsh[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Four,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Four,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

    elif year == 2011:
        # regions for 2011 are east, southeast, southwest, west
        est = soup.find_all("div", {"id": "east"})
        se = soup.find_all("div", {"id": "southeast"})
        sw = soup.find_all("div", {"id": "southwest"})
        west = soup.find_all("div", {"id": "west"})

        # Get data for all teams in east region
        rounds = est[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("One,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            # lower seed second
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            logging.info("make_yearfile: %s", links[2].text)
            f.write("One,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

        # Get data for all teams in southeast region
        rounds = se[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Two,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Two,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

            # Get data for all teams in southwest region
        rounds = sw[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Three,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Three,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

            # Get data for all teams in west region
        rounds = west[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Four,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Four,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

    else:
        # all other years in range have regions east, south, midwest, west
        east = soup.find_all("div", {"id": "east"})
        south = soup.find_all("div", {"id": "south"})
        midwest = soup.find_all("div", {"id": "midwest"})
        west = soup.find_all("div", {"id": "west"})

        # Get data for all teams in east region
        rounds = east[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("One,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # Lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("One,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

        # Get data for all teams in south region
        rounds = south[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Two,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Two,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

        # Get data for all teams in midwest region
        rounds = midwest[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            # Higher seed first
            links = game.find_all("a")
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Three,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Three,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

            # Get data for all teams in west region
        rounds = west[0].find_all("div", {"class": "round"})
        rd = rounds[0]
        games = rd.find_all("div")
        for j in range(0, 24, 3):
            game = games[j]
            spans = game.find_all("span")
            links = game.find_all("a")
            # Higher seed first
            logging.info("make_yearfile: %s", links[0].text)
            f.write("Four,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[0].text + ",")  # higher seed
            f.write(links[0].text + ",")  # name
            f.write(links[1].text + ",")  # score
            team_url = sports_ref_url + links[0].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")
            # lower seed second
            logging.info("make_yearfile: %s", links[2].text)
            f.write("Four,")  # Bracket Region
            f.write(links[4].text + ",")  # game location
            f.write(spans[1].text + ",")  # lower seed
            f.write(links[2].text + ",")  # name
            f.write(links[3].text + ",")  # score
            team_url = sports_ref_url + links[2].get("href")
            logging.info("make_yearfile: getting response from: " + team_url)
            stats = get_team_stats(team_url)
            write_team_stats(f, stats)
            f.write("\n")

    # Done writing data to file 
    f.close()
    logging.info("make_yearfile: exiting")

# Uncomment the below lines to write csv files for all years 2001-2017

# for year in range(2001, 2018, 1):
#    make_yearfile(year)
