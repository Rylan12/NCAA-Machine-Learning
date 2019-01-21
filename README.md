# NCAA
###### Created by Kevin Nowland and Matthew Osborne
###### Adaptation by Rylan Polster
In this repository is python code used to scrape 2001-2017 ncaa first round tournament data from https://www.sports-reference.com/cbb/. Descriptions of the basketball statistics can be found on that site. Additionally, we have included the data file we managed to scrape and then clean for our purposes. The variables in this csv file can be found below.

## Usage
1. Change `current_year` on line 166 of `make_datafile.py` to the current year
2. Run `make_datafile.py`
3. Change line 211 in `model.py` to reflect the year you want to check
4. Run `model.py`

## Variable description for NCAA2001_2017.csv
year - This is the year that the tournament took place, values 2001-2017

SeedType - This is the seeding of the game. For example, OneSixteen  means it was the 1st seed vs the 16th seed.

Upset - This variable indicates whether or not this game was an upset. Meaning the lower seed beat the higher seed. 0 indicates no upset occurred, 1 indicates an upset occurred

Region - The bracket is broken into four regions every year. This variable tracks which of the four regions the game took place in. 

GameCity - City where the game was played.

GameState - State where the game was played.

TopSeed - The higher seeded team.

TopCity - Hometown of the higher seeded team.

TopST - Home state of the higher seeded team.

TopTravel - Distance traveled by the higher seeded team in km.

TopScore - The score of the higher seeded team in the first round game.

TopGames - Number of games played by the higher seeded team, -9999 indicates a missing value.

TopFG - Field goals made by the higher seeded team, -9999 indicates a missing value.

TopFGA - Field goals attempted by the higher seeded team, -9999 indicates a missing value.

TopFGPerc - Field goal percentage of the higher seeded team, -9999 indicates a missing value.

Top3P - 3 pters made by the higher seeded team, -9999 indicates a missing value.

Top3PA - 3 pters attempted by the higher seeded team, -9999 indicates a missing value.

Top3Per - 3 pt percentage of the higher seeded team, -9999 indicates a missing value.

Top2P - 2 pters made by the higher seeded team, -9999 indicates a missing value.

Top2PA - 2 pters attempted by the higher seeded team, -9999 indicates a missing value.

Top2Per - 3 pt percentage of the higher seeded team, -9999 indicates a missing value.

TopPTs - Total points scored by the higher seeded team, -9999 indicates a missing value.

TopOppPTS - Total points allowed by the higher seeded team, -9999 indicates a missing value.

TopAST - Total assists by the higher seeded team, -9999 indicates a missing value.

TopORB - Total offensive rebounds by the higher seeded team, -9999 indicates a missing value.

TopDRB - Total defensive rebounds by the higher seeded team, -9999 indicates a missing value.

TopPoss - Total estimated possessions by the higher seeded team, -9999 indicates a missing value.

TopTSPer - True shooting percentage by the higher seeded team, -9999 indicates a missing value.

TopEFGPer - Effective field goal percentage by the higher seeded team, -9999 indicates a missing value.

TopTOV - Total turnovers by the higher seeded team, -9999 indicates a missing value.

TopTOPer - Turnover percentage of the higher seeded team, -9999 indicates a missing value.

TopFT - Total free throws taken by the higher seeded team, -9999 indicates a missing value.

TopFTA - Total free throws attempted by the higher seeded team, -9999 indicates a missing value.

TopFTR - Free throw rate of the higher seeded team, -9999 indicates a missing value.

TopORTG - Offensive rating of the higher seeded team, -9999 indicates a missing value.

TopDRTG - Defensive rating of the higher seeded team, -9999 indicates a missing value.

TopSOS - Strength of Schedule of the higher seeded team, -9999 indicates a missing value.

BotSeed - The lower seeded team.

BotCity - Hometown of the lower seeded team.

BotST - Home State of the lower seeded team.

BotTravel - Distance traveled by the lower seeded team in km.

BotScore - The score of the lower seeded team in the first round game.

BotGames - Number of games played by the lower seeded team, -9999 indicates a missing value.

BotFG - Field goals made by the lower seeded team, -9999 indicates a missing value.

BotFGA - Field goals attempted by the lower seeded team, -9999 indicates a missing value.

BotFGPerc - Field goal percentage of the lower seeded team, -9999 indicates a missing value.

Bot3P - 3 pters made by the lower seeded team, -9999 indicates a missing value.

Bot3PA - 3 pters attempted by the lower seeded team, -9999 indicates a missing value.

Bot3Per - 3 pt percentage of the lower seeded team, -9999 indicates a missing value.

Bot2P - 2 pters made by the lower seeded team, -9999 indicates a missing value.

Bot2PA - 2 pters attempted by the lower seeded team, -9999 indicates a missing value.

Bot2Per - 3 pt percentage of the lower seeded team, -9999 indicates a missing value.

BotPTs - Total points scored by the lower seeded team, -9999 indicates a missing value.

BotOppPTS - Total points allowed by the lower seeded team, -9999 indicates a missing value.

BotAST - Total assists by the lower seeded team, -9999 indicates a missing value.

BotORB - Total offensive rebounds by the lower seeded team, -9999 indicates a missing value.

BotDRB - Total defensive rebounds by the lower seeded team, -9999 indicates a missing value.

BotPoss - Total estimated possessions by the lower seeded team, -9999 indicates a missing value.

BotTSPer - True shooting percentage by the lower seeded team, -9999 indicates a missing value.

BotEFGPer - Effective field goal percentage by the lower seeded team, -9999 indicates a missing value.

BotTOV - Total turnovers by the lower seeded team, -9999 indicates a missing value.

BotTOPer - Turnover percentage of the lower seeded team, -9999 indicates a missing value.

BotFT - Total free throws taken by the lower seeded team, -9999 indicates a missing value.

BotFTA - Total free throws attempted by the lower seeded team, -9999 indicates a missing value.

BotFTR - Free throw rate of the lower seeded team, -9999 indicates a missing value.

BotORTG - Offensive rating of the lower seeded team, -9999 indicates a missing value.

BotDRTG - Defensive rating of the lower seeded team, -9999 indicates a missing value.

BotSOS - Strength of Schedule of the lower seeded team, -9999 indicates a missing value.
