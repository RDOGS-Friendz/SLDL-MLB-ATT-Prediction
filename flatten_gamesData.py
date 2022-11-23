import pandas as pd
import pickle
import calendar
import re

from itertools import islice

precipitation_values_list = [" Drizzle.", " No Precipitation.", " Rain."]

usa_federal_holidays = {
    '2015': ['1/1', '1/19', '2/16', '5/25', '7/4', '9/7', '10/12', '11/11' '11/26', '12/25'],
    '2016': ['1/1', '1/18', '2/15', '5/30', '7/4', '9/5', '10/10', '11/11', '11/24', '12/26'],
    '2017': ['1/1', '1/2', '1/16', '2/20', '5/29', '7/4', '9/4', '10/9', '11/10', '11/11', '11/23', '12/25'],
    '2018': ['1/1', '1/15', '2/19', '5/28', '7/4', '9/3', '10/8', '11/11', '11/12', '11/22', '12/25'],
    '2019': ['1/1', '1/21', '2/18', '5/27', '7/4', '9/2', '10/14', '11/11', '11/28', '12/25'],
    '2020': ['1/1', '1/20', '2/17', '5/25', '7/3', '7/4', '9/7', '10/12', '11/11', '11/26', '12/25'],
    '2021': ['1/1', '1/18', '2/15', '5/31', '6/18', '6/19', '7/4', '7/5', '9/6', '10/11', '11/11', '11/25', '12/24', '12/25', '12/31'],
    '2022': ['1/1', '1/17', '2/21', '5/30', '6/19', '6/20', '7/4', '9/5', '10/10', '11/11', '11/24', '12/25', '12/26']
}

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def flatten_games(games, year):
    games_flatten = {}
    holiday_list = usa_federal_holidays[year]

    # create a dictionary, key is unique team name, value is their streak which is default to 0
    teams_streak = {}
    unique_team_names = set()
    for game_id in games.keys():
        # get team1 name and team2 name and add them to unique_team_names
        unique_team_names.add(games[game_id]['team1']['name'])
        unique_team_names.add(games[game_id]['team2']['name'])
    
    # add unique team names to teams_streak
    for team_name in unique_team_names:
        teams_streak[team_name] = {
            'pre_win': 0,
            'pre_loss': 0,
            'cumulative_streak': 0
        }

    for game_id in games.keys():
        games_flatten[game_id] = {}
        games_flatten[game_id]['game_page_url'] = game_id
        games_flatten[game_id]['have_att'] = games[game_id]['meta_game_info']['have_att']
        games_flatten[game_id]['start_time'] = games[game_id]['meta_game_info']['start_time']
        
        # default value
        day = 1
        month = 1
        try:
            day = calendar.day_name[games[game_id]['meta_game_info']['start_time'].weekday()]
            month = calendar.month_name[games[game_id]['meta_game_info']['start_time'].month]
        except:
            # game_id is the url of the game page and we can use regex to get numeric part of the url and use it as day and month
            # example: https://www.baseball-reference.com/boxes/CHN/CHN201904010.shtml
            # get numeric part of the url
            numeric_part = re.findall(r'\d+', game_id)
            # get day and month
            # get substring of the numeric part
            day = int(numeric_part[0][6:8])
            month = int(numeric_part[0][4:6])

        date_str = f"{month}/{day}"
        games_flatten[game_id]['day'] = day
        games_flatten[game_id]['month'] = month
        games_flatten[game_id]['is_federal_holiday'] = 1 if date_str in holiday_list else 0
        games_flatten[game_id]['duration'] = games[game_id]['meta_game_info']['duration']
        games_flatten[game_id]['venue'] = games[game_id]['meta_game_info']['venue']
        games_flatten[game_id]['at_night'] = games[game_id]['meta_game_info']['at_night']
        games_flatten[game_id]['on_grass'] = games[game_id]['meta_game_info']['on_grass']
        games_flatten[game_id]['weather_description'] = games[game_id]['meta_game_info']['Start Time Weather']
        
        # default value for weather factors
        temperature = 0
        wind_speed = 0
        weather = 'Sunny'
        precipitation = 0

        try:
            temperature = int(re.findall(r'\d+', games[game_id]['meta_game_info']['Start Time Weather'].split(',')[0])[0])
            # use regex to get wind speed, which is only number in the string
            wind_speed = int(re.findall(r'\d+', games[game_id]['meta_game_info']['Start Time Weather'].split(',')[1])[0])
            weather = (games[game_id]['meta_game_info']['Start Time Weather'].split(',')[2]).strip()
        except:
            print(f"cannot get temperature and wind_speed from weather description: {games[game_id]['meta_game_info']['Start Time Weather']}, automatically set to 0")
        
        # get comma count in Start Time Weather
        comma_count = games[game_id]['meta_game_info']['Start Time Weather'].count(',')

        if comma_count < 3:
            precipitation = 4
        else:
            precipitation_str = games[game_id]['meta_game_info']['Start Time Weather'].split(',')[3]
            match_index = -1
            for i in range(len(precipitation_values_list)):
                if precipitation_values_list[i] == precipitation_str:
                    match_index = i
                    break
            precipitation = match_index
            # ensure precipitation is in range 0 to 3
            if precipitation == -1:
                # something wrong with precipitation, use input to get precipitation
                print(f"cannot get precipitation from weather description: {games[game_id]['meta_game_info']['Start Time Weather']}")
                precipitation = input("please input precipitation: ")

        games_flatten[game_id]['temperature'] = temperature
        games_flatten[game_id]['wind_speed'] = wind_speed
        games_flatten[game_id]['weather'] = weather
        games_flatten[game_id]['precipitation'] = precipitation
        games_flatten[game_id]['umpires'] = games[game_id]['meta_game_info']['Umpires']
        games_flatten[game_id]['attendance'] = games[game_id]['meta_game_info']['att']
        games_flatten[game_id]['team1_name'] = games[game_id]['team1']['name']
        games_flatten[game_id]['team1_pre_win'] = games[game_id]['team1']['pre_win']
        games_flatten[game_id]['team1_pre_loss'] = games[game_id]['team1']['pre_loss']
        # win_pct = win / (win + loss)
        if games[game_id]['team1']['pre_win'] + games[game_id]['team1']['pre_loss'] == 0:
            games_flatten[game_id]['team1_pre_win_pct'] = 0
        else:
            games_flatten[game_id]['team1_pre_win_pct'] = games[game_id]['team1']['pre_win'] / (games[game_id]['team1']['pre_win'] + games[game_id]['team1']['pre_loss'])
        games_flatten[game_id]['team1_players'] = games[game_id]['team1']['player_df']

        if games[game_id]['team1']['pre_win'] > teams_streak[games[game_id]['team1']['name']]['pre_win']:
            if teams_streak[games[game_id]['team1']['name']]['cumulative_streak'] < 0:
                teams_streak[games[game_id]['team1']['name']]['cumulative_streak'] = 1
            else:
                teams_streak[games[game_id]['team1']['name']]['cumulative_streak'] += 1
            games_flatten[game_id]['team1_streak'] = teams_streak[games[game_id]['team1']['name']]['cumulative_streak']
        elif games[game_id]['team1']['pre_loss'] > teams_streak[games[game_id]['team1']['name']]['pre_loss']:
            if teams_streak[games[game_id]['team1']['name']]['cumulative_streak'] > 0:
                teams_streak[games[game_id]['team1']['name']]['cumulative_streak'] = -1
            else:
                teams_streak[games[game_id]['team1']['name']]['cumulative_streak'] -= 1
            games_flatten[game_id]['team1_streak'] = teams_streak[games[game_id]['team1']['name']]['cumulative_streak']
        else:
            games_flatten[game_id]['team1_streak'] = 0

        teams_streak[games[game_id]['team1']['name']]['pre_win'] = games[game_id]['team1']['pre_win']
        teams_streak[games[game_id]['team1']['name']]['pre_loss'] = games[game_id]['team1']['pre_loss']
        
        # for team2 do the same thing
        games_flatten[game_id]['team2_name'] = games[game_id]['team2']['name']
        games_flatten[game_id]['team2_pre_win'] = games[game_id]['team2']['pre_win']
        games_flatten[game_id]['team2_pre_loss'] = games[game_id]['team2']['pre_loss']
        if games[game_id]['team2']['pre_win'] + games[game_id]['team2']['pre_loss'] == 0:
            games_flatten[game_id]['team2_pre_win_pct'] = 0
        else:
            games_flatten[game_id]['team2_pre_win_pct'] = games[game_id]['team2']['pre_win'] / (games[game_id]['team2']['pre_win'] + games[game_id]['team2']['pre_loss'])
        games_flatten[game_id]['team2_players'] = games[game_id]['team2']['player_df']

        if games[game_id]['team2']['pre_win'] > teams_streak[games[game_id]['team2']['name']]['pre_win']:
            if teams_streak[games[game_id]['team2']['name']]['cumulative_streak'] < 0:
                teams_streak[games[game_id]['team2']['name']]['cumulative_streak'] = 1
            else:
                teams_streak[games[game_id]['team2']['name']]['cumulative_streak'] += 1
            games_flatten[game_id]['team2_streak'] = teams_streak[games[game_id]['team2']['name']]['cumulative_streak']
        elif games[game_id]['team2']['pre_loss'] > teams_streak[games[game_id]['team2']['name']]['pre_loss']:
            if teams_streak[games[game_id]['team2']['name']]['cumulative_streak'] > 0:
                teams_streak[games[game_id]['team2']['name']]['cumulative_streak'] = -1
            else:
                teams_streak[games[game_id]['team2']['name']]['cumulative_streak'] -= 1
            games_flatten[game_id]['team2_streak'] = teams_streak[games[game_id]['team2']['name']]['cumulative_streak']
        else:
            games_flatten[game_id]['team2_streak'] = 0

        teams_streak[games[game_id]['team2']['name']]['pre_win'] = games[game_id]['team2']['pre_win']
        teams_streak[games[game_id]['team2']['name']]['pre_loss'] = games[game_id]['team2']['pre_loss']

    return games_flatten
        
if __name__ == "__main__":
    # combine all games from 2015 to 2022 except 2020 and 2021
    games = {}
    for year in range(2015, 2022):
        print(year)
        if year == 2020 or year == 2021:
            continue
        cur_year_games = pd.read_pickle(f"gamesData{year}.pickle")
        cur_year_flatten_games = flatten_games(cur_year_games, str(year))
        games.update(cur_year_flatten_games)
    # print out the total number of games
    print(f"Total number of games: {len(games)}")
    # save the games to a pickle file
    with open("trainset.pickle", "wb") as f:
        pickle.dump(games, f)
    
    # for 2022
    games = {}
    cur_year_games = pd.read_pickle(f"gamesData2022.pickle")
    cur_year_flatten_games = flatten_games(cur_year_games, str(year))
    games.update(cur_year_flatten_games)
    with open("testset.pickle", "wb") as f:
        pickle.dump(games, f)
    print("Done!")