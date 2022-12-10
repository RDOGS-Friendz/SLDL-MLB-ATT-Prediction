import pandas as pd
from pprint import pprint
from typing import NamedTuple, List, TypedDict
import datetime
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler


class InputInfo(TypedDict):
    date: datetime.date
    start_hour: int
    home_team: str
    away_team: str
    weather: str
    temperature: float
    season_type: bool


# afternoon, evening, night, noon
### -13 noon 14-16 afternoon 17-19 evening 20- night
def streamlit_to_model(data: InputInfo) -> List:
    df = pd.read_csv("models-v2-lle/testset_w_lle.csv")

    with open("testset.pickle", "rb") as f:
        d = pickle.load(f)
    temperature_data = list()

    for key in d.keys():
        temperature_data.append([d[key]["temperature"]])

    xscaler_temperature = StandardScaler().fit(np.array(temperature_data))
    xscaler_ma = StandardScaler().fit(df[["previous_5_to_10MA"]])
    # print(xscaler_temperature.transform([[70]]))

    team_set = set(df["team1_name"])
    ret = list()
    # holiday       todo:      flatten_gamesData.py
    ret.append(0)
    # on_grass
    ret.append(df[df["team2_name"] == data["home_team"]].iloc[0]["on_grass"])
    ret.append(
        xscaler_temperature.transform(np.array(data["temperature"]).reshape(-1, 1))[0][
            0
        ]
    )
    # team_1 name, pre_win, pre_loss, pre_win_pct, streak
    # ret.append(data["away_team"])
    last_data = df[
        (df["team1_name"] == data["away_team"]) & (df["start_time"] < str(data["date"]))
    ].iloc[-1]
    ret.append(last_data["team1_pre_win"])
    ret.append(last_data["team1_pre_loss"])
    ret.append(last_data["team1_pre_win_pct"])
    ret.append(last_data["team1_streak"])

    # team 2
    # ret.append(data["home_team"])
    last_data = df[
        (df["team2_name"] == data["home_team"]) & (df["start_time"] < str(data["date"]))
    ].iloc[-1]
    ret.append(last_data["team2_pre_win"])
    ret.append(last_data["team2_pre_loss"])
    ret.append(last_data["team2_pre_win_pct"])
    ret.append(last_data["team2_streak"])

    # salary

    ret.append(0)
    ret.append(0)
    ret.append(0)

    # weekday 5 1 6 7 4 2 3
    day_transfer = [4, 0, 5, 6, 3, 1, 2]
    weekday = data["date"].weekday()
    day_post = [1 if i == weekday else 0 for i in day_transfer]

    ret += day_post
    # month 4, 8, 7, 6, 3, 5, 11, 10, 9
    month_transfer = [4, 8, 7, 6, 3, 5, 11, 10, 9]
    month = data["date"].month
    month_post = [1 if i == month else 0 for i in month_transfer]
    ret += month_post

    # 'weather_Cloudy', 'weather_Drizzle', 'weather_In Dome',
    # 'weather_Overcast', 'weather_Rain', 'weather_Sunny'

    weather_transfer = ["Cloudy", "Drizzle", "In_Dome", "Overcast", "Rain", "Sunny"]
    weather_post = [1 if i == data["weather"] else 0 for i in weather_transfer]
    ret += weather_post
    # ret.append(int(data["season_type"]))
    # ?seas
    ret.append(data["date"].year)
    # home_team_avg_last_year
    ret.append(
        df[df["team2_name"] == data["home_team"]].iloc[0]["home_team_avg_att_last_year"]
    )
    # afternoon, evening, night, noon
    ### -13 noon 14-16 afternoon 17-19 evening 20- night
    start_time_list = [0, 0, 0, 0]
    if data["start_hour"] <= 13:
        start_time_list[3] = 1
    elif data["start_hour"] <= 16:
        start_time_list[0] = 1
    elif data["start_hour"] <= 19:
        start_time_list[1] = 1
    else:
        start_time_list[2] = 1
    ret += start_time_list

    # previous 5-10
    last_data = df[
        (df["team2_name"] == data["home_team"]) & (df["start_time"] > str(data["date"]))
    ].iloc[0]
    ret.append(xscaler_ma.transform([[last_data["previous_5_to_10MA"]]])[0][0])

    # lle
    ret.append(0)
    ret.append(0)

    # team1 name dummy
    team_list = list(team_set)
    team_list.sort()
    ret += [1 if team == data["away_team"] else 0 for team in team_list]
    ret += [1 if team == data["home_team"] else 0 for team in team_list]

    # team2 name dummy
    if data["season_type"] == True:
        ret += [1, 0]
    else:
        ret += [0, 1]
    # season type   post, regular

    return ret


class Model(object):
    def __init__(self, type: str):
        # path = "../models-v2-lle/lasso_model_20221204_235019.sav"
        path = {
            "XGBoost": "models-v2-lle/model/xgboost_model_20221207_235653.sav",
            "Stacking": "models-v2-lle/model/stacking_model_20221204_214116.sav",
            "Ridge": "models-v2-lle/model/ridge_model_20221207_235056.sav",
            "Gradient Boosting": "models-v2-lle/model/gradientboosting_model_20221207_235438.sav",
            "SVM": "models-v2-lle/model/svm_model_20221207_235128.sav"
        }
        with open(path[type], "rb") as f:
            self.model = pickle.load(f)

    def predict(self, data):
        print(data)
        data = np.array(data).reshape(1, -1)
        return self.model.predict(data)


model = Model("Stacking")

r = streamlit_to_model(
    {
        "date": datetime.date(2022, 7, 13),
        "start_hour": 15,
        "home_team": "TOR",
        "away_team": "ATL",
        "weather": "Sunny",
        "temperature": 35.2,
        "season_type": True,
    }
)


print(model.predict(r))
