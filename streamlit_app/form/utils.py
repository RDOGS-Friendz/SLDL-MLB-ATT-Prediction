from collections import defaultdict, namedtuple
from htbuilder import div, big, h2, styles, hr
from htbuilder.units import rem
from math import floor
import altair as alt
import datetime
import functools
import pandas as pd
import re
import streamlit as st
import time


def create_form(team_lst: list, weather_lst: list, model_lst: list, baseline_model_lst: list):

    # input
    """
    兩隊
    比賽時間 (yyyyMMdd HH)
    主場球隊是誰
    """

    with st.form(key="my_form"):

        error_flag = False
        # --------------------------------------------------------------------------------------------------
        # Draw app inputs

        input_params = {}

        col_1, col_2 = st.columns([1, 1])

        # date
        game_date = col_1.date_input(
            "Game date",
            datetime.date(2022, 7, 6), min_value=datetime.date(2022, 4, 7), max_value=datetime.date(2022, 11, 5))

        # time
        game_time = col_2.time_input("Game time", datetime.time(20, 0))
        game_datetime = datetime.datetime.combine(
            game_date, game_time)  # type: ignore

        input_params["date"] = game_date
        input_params["time"] = int(game_time.strftime("%H"))
        input_params["datetime"] = game_datetime

        # season type
        input_params["season_type"] = st.checkbox("Playoff", value=False)

        # home team and away team
        col_1, col_2 = st.columns([1, 1])
        st.selectbox
        input_params["home_team"] = col_1.selectbox(
            "Select home team", team_lst, index=0)
        input_params["away_team"] = col_2.selectbox(
            "Select away team", team_lst, index=1)
        if input_params["home_team"] == input_params["away_team"]:
            st.error("Home team and away team cannot be the same.")
            error_flag = True
            # st.stop()

        col_1, col_2 = st.columns([1, 1])

        # weather
        input_params["weather"] = col_1.selectbox(
            "Select weather", weather_lst, index=len(weather_lst)-1)

        # temperature
        input_params["temperature"] = col_2.number_input(
            "Temperature (°F)", min_value=-20.0, max_value=200.0, value=70.0, step=0.1, format="%.1f")

        # input_params["stadium"] = st.selectbox(
        #     "Select stadium", ['[default]'] + stadium_lst, help="[default] will automatically select the stadium based on the selected home team.")

        # models
        input_params["model"] = st.multiselect(
            "Select prediction model(s)", model_lst, help="Select one or more models to predict the game outcome. A maximum of 3 models can be selected.", default=model_lst[0], max_selections=3)

        if len(input_params["model"]) == 0:
            st.error("At least one model must be selected.")
            error_flag = True
            # st.stop()

        # st.markdown(
        #     div(
        #         style=styles(
        #             # center
        #             text_align="center",
        #             # small font
        #             font_size=rem(0.8),
        #             # gray color
        #             color="#666666",
        #         )
        #     )("Please fill all the fields above"), unsafe_allow_html=True)

        # st.markdown(
        #     hr(
        #         style=styles(
        #             margin=(rem(.5), 0, rem(1), 0),
        #             # height=rem(0.1),
        #             # color=PRIMARY_COLOR,
        #             # background_color=PRIMARY_COLOR,
        #         )
        #     ),
        #     unsafe_allow_html=True,
        # )

        # input_params["baseline_model"] = st.multiselect(
        #     "Select baseline model(s)", baseline_model_lst, help="Baseline models are used to compare with the prediction models. A maximum of two baseline models can be selected. Leave blank if you don't need any comparisons.", max_selections=2)

        # col_1, col_2, col_3 = st.columns([1, 2, 1])
        # input_params["enable_PCA"] = col_1.checkbox(
        #     "Enable PCA", False)

        submit_button = st.form_submit_button(label="Submit")

    if submit_button and not error_flag:
        return input_params
    elif submit_button and error_flag:
        st.stop()
    else:
        return input_params
