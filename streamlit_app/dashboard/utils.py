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
