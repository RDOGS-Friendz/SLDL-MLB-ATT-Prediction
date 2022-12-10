from collections import defaultdict, namedtuple
from htbuilder import div, big, h2, styles
from htbuilder.units import rem
from math import floor
import altair as alt
import datetime
import functools
import pandas as pd
import numpy as np
import re
import streamlit as st
import time
import plotly.express as px
from vega_datasets import data
from st_aggrid import AgGrid
from pprint import pprint
from typing import NamedTuple, List, TypedDict
import datetime

# rm 'venue', 'start_hour', 'start_time', 'game_page_url'

# ['attendance', 'is_federal_holiday', 'venue', 'on_grass', 'temperature',
# 'team1_name', 'team1_pre_win', 'team1_pre_loss', 'team1_pre_win_pct',
# \'team1_streak', 'team2_name', 'team2_pre_win', 'team2_pre_loss', 'team2_pre_win_pct',
# 'team2_streak', 'salary-500-800', 'salary-800-1500', 'salary-1500',
# 'day_Friday', 'day_Monday', 'day_Saturday', 'day_Sunday', 'day_Thursday',
# 'day_Tuesday', 'day_Wednesday', 'month_April', 'month_August', 'month_July',
# 'month_June', 'month_March', 'month_May', 'month_November', 'month_October',
# \'month_September', 'weather_Cloudy', 'weather_Drizzle', 'weather_In Dome',
# 'weather_Overcast', 'weather_Rain', 'weather_Sunny', 'season_type', 'season',
# 'home_team_avg_att_last_year', 'start_hour', 'start_hour_label_afternoon',
# 'start_hour_label_evening', 'start_hour_label_night', 'start_hour_label_noon', 'game_page_url',
# 'start_time', 'previous_5_to_10MA', 'lle1', 'lle2']


class InputInfo(TypedDict):
    date: datetime.date
    start_hour: int
    home_team: str
    away_team: str
    weather: str
    temperature: float
    season_type: bool

# afternoon, evening, night, noon
# -13 noon 14-16 afternoon 17-19 evening 20- night


def st_to_model(data: InputInfo, df: pd.DataFrame, team_set: set) -> List:
    # df = pd.read_csv("../models-v2-lle/testset_w_lle.csv")
    # team_set = set(df["team1_name"])

    ret = list()
    # holiday       todo:      flatten_gamesData.py
    ret.append(0)
    # on_grass
    ret.append(df[df["team2_name"] == data["home_team"]].iloc[0]["on_grass"])
    ret.append(data["temperature"])
    # team_1 name, pre_win, pre_loss, pre_win_pct, streak
    # ret.append(data["away_team"])
    last_data = df[(df["team1_name"] == data["away_team"]) & (
        df["start_time"] < str(data["date"]))].iloc[-1]
    ret.append(last_data["team1_pre_win"])
    ret.append(last_data["team1_pre_loss"])
    ret.append(last_data["team1_pre_win_pct"])
    ret.append(last_data["team1_streak"])

    # team 2
    # ret.append(data["home_team"])
    last_data = df[(df["team2_name"] == data["home_team"]) & (
        df["start_time"] < str(data["date"]))].iloc[-1]
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

    weather_transfer = ["Cloudy", "Drizzle",
                        "In_Dome", "Overcast", "Rain", "Sunny"]
    weather_post = [1 if i == data["weather"] else 0 for i in weather_transfer]
    ret += weather_post
    # ret.append(int(data["season_type"]))
    # ?seas
    ret.append(data["date"].year)
    # home_team_avg_last_year
    ret.append(df[df["team2_name"] == data["home_team"]].iloc[0]
               ["home_team_avg_att_last_year"])

    # afternoon, evening, night, noon
    # -13 noon 14-16 afternoon 17-19 evening 20- night
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
    last_data = df[(df["team2_name"] == data["home_team"]) &
                   (df["start_time"] > str(data["date"]))].iloc[0]
    ret.append(last_data["previous_5_to_10MA"])

    # lle
    ret.append(0)
    ret.append(0)

    # team1 name dummy
    team_list = list(team_set)
    ret += [1 if team == data["away_team"] else 0 for team in team_list]
    ret += [1 if team == data["home_team"] else 0 for team in team_list]

    # team2 name dummy
    if data["season_type"] == True:
        ret += [1, 0]
    else:
        ret += [0, 1]
    # season type   post, regular

    return ret


def ma_chart(df: pd.DataFrame, date_str: str = 'date', attendance_str: str = 'attendance', ma_str: str = 'previous_5_to_10MA', color: object = None):
    source = df.copy()

    bar = alt.Chart(source).mark_bar(color=color.BLUE).encode(  # type: ignore
        x=alt.X(f'yearmonthdate({date_str}):O', axis=alt.Axis(  # type: ignore
            title='Date', labelAngle=15)),  # type: ignore
        y=alt.Y(f'{attendance_str}:Q', axis=alt.Axis(  # type: ignore
            title='Attendance')),  # type: ignore
        tooltip=[
            alt.Tooltip(f'{attendance_str}',  # type: ignore
                        title='Attendance'),  # type: ignore
            alt.Tooltip(f'{ma_str}',  # type: ignore
                        title='Previous 5-10 MA'),  # type: ignore
            alt.Tooltip(f'{date_str}', title='Date'),  # type: ignore
        ]
    )

    line = alt.Chart(source).mark_line(color=color.RED).encode(  # type: ignore
        x=f'{date_str}:T',
        y=f'{ma_str}:Q',
    )

    tmp_plt = (bar + line).interactive()
    # altair_viewer.display(tmp_plt, inline=True)
    return tmp_plt


def ft_imp_chart(model_df: pd.DataFrame, num_of_feature: int = 10, color: object = None):
    source = model_df.copy().iloc[:num_of_feature, :]

    tmp_plt = alt.Chart(source).mark_bar(color=color.BLUE).encode(  # type: ignore
        x='Metric:Q',
        y=alt.Y('Processed Feature Name:N', sort='-x',  # type: ignore
                axis=alt.Axis(labelLimit=100)),  # type: ignore
        tooltip=[
            'Model',
            'Metric',
            alt.Tooltip('Processed Feature Name',  # type: ignore
                        title='Feature Name'),  # type: ignore
            alt.Tooltip('Feature', title='Raw Feature Name'),  # type: ignore

        ]
    )

    # altair_viewer.display(tmp_plt, inline=True)
    return tmp_plt


def get_baseline_value(df_home: pd.DataFrame, date_str: str, team_name: str):
    def nearest(items, pivot):
        target_date = pd.to_datetime(
            min([i for i in items if i <= pivot], key=lambda x: abs(x - pivot)))
        return target_date

    date_str = np.datetime64(date_str)  # type: ignore
    # team_name = "ARI"

    # get baseline value
    target_date = nearest(df_home['date'].values, date_str)

    baseline_value = df_home[(df_home["date"] == target_date) & (
        df_home["team2_name"] == team_name)]["previous_5_to_10MA"].values[0]
    return target_date, baseline_value
