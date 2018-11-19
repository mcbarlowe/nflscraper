'''
These will be the helper functions for the main scraper to use to parse the
NFL play by play
'''

import re
import requests
import bs4
import pandas as pd

def scrape_week(season, week):
    '''
    this function scrapes the NFL schedule for the season and week of season
    passed and returns the game id, home team, away team, date and week

    Inputs:
    season - (integer) the year of the NFL season to scrape results
    week - (integer) week in the nfl season to get

    Outputs:
    sched_df - (dataframe) pandas dataframe containing the
               features scraped from the schedule
    '''

    base_url = 'http://www.nfl.com/schedules/'

    games = []
    #get nfl schedule
    req = requests.get(f'{base_url}{season}/REG{week}')
    soup = bs4.BeautifulSoup(req.text, 'lxml')

    #get all the links from the schedule and pull out the game id
    #and home and away team
    a_tags = (soup.select('div[class="list-matchup-row-gc-link"] a'))

    #this breaks down each url of the game using regex to pull out the game_id
    #home_team, away_team, date, and week
    games.extend([[re.search("[0-9]{10}", x['href']).group(0),
                  re.search("[a-z0-9]+@[a-z0-9]+", x['href']).group(0).split('@')[0],
                  re.search("[a-z0-9]+@[a-z0-9]+", x['href']).group(0).split('@')[1],
                  re.search("[0-9]{10}", x['href']).group(0)[:8], week] for x in a_tags])

    #convert the lists created from the scraped urls into a dataframe
    sched_df = pd.DataFrame(games, columns=['game_id', 'away_team', 'home_team', 'date', 'week'])

    return sched_df


def scrape_season(season):
    '''
    this function will scrape the schedule to get the game ids of an entire
    season and return the results as a pandas dataframe

    Inputs:
    season - (integer) the year of the NFL season to be scraped

    Outputs:
    season_df - (dataframe) pandas dataframe of the full nfl season
    '''

    weeks_dfs = []

    for week in range(1, 18):
        try:
            weeks_dfs.append(scrape_week(season, week))
        except AttributeError as e:
    #catches error when trying to scrape schedule of games that have not been
    #played yet because the NFL doesn't assign game ids to unplayed games
            break

    season_df = pd.concat(weeks_dfs)

    return season_df

