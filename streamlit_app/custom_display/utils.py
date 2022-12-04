from collections import defaultdict, namedtuple
from htbuilder import div, big, h2, styles
from htbuilder.units import rem
from math import floor
import altair as alt
import datetime
import functools
import pandas as pd
import re
import streamlit as st
import time


def display_callout(title, color, icon, second_text):
    st.markdown(
        div(
            style=styles(
                background_color=color,
                padding=rem(1),
                display="flex",
                flex_direction="row",
                border_radius=rem(0.5),
                margin=(0, 0, rem(0.5), 0),
            )
        )(
            div(style=styles(font_size=rem(2), line_height=1))(icon),
            div(style=styles(padding=(rem(0.5), 0, rem(0.5), rem(1))))(title),
        ),
        unsafe_allow_html=True,
    )


def display_small_text(text):
    st.markdown(
        div(
            style=styles(
                font_size=rem(0.8),
                margin=(0, 0, rem(1), 0),
            )
        )(text),
        unsafe_allow_html=True,
    )


def display_dial(title, value, color, delta=None):
    if delta is not None:
        if delta > 0:
            # green
            delta_color = "#0A9B37"
            prefix = '\u2191'
        elif delta == 0:
            # gray
            delta_color = "#808080"
            prefix = ''
        else:
            # red
            delta_color = "#DD2728"
            prefix = '\u2193'
        delta_div = div(style=styles(
            font_size=rem(0.9),
            color=delta_color,
            margin=(rem(.8), 0, 0, 0),
        ))(f"{prefix} {delta:,}")  # format with comma
    else:
        delta_div = ""

    st.markdown(
        div(
            style=styles(
                text_align="center",
                color=color,
                padding=(rem(0.8), 0, rem(3), 0),
            )
        )(
            h2(style=styles(font_size=rem(.975),
                            font_weight=600, padding=0))(title),
            big(style=styles(font_size=rem(3), font_weight=800, line_height=1))(
                value
            ),
            delta_div
        ),
        unsafe_allow_html=True,
    )


def display_dict(dict):
    for k, v in dict.items():
        a, b = st.columns([1, 4])
        a.write(f"**{k}:**")
        b.write(v)


def display_team_info(team):
    team_info = {
        "Team name": team["team_name"],
        "Abbr.": team["team_abbr"],
        "Home stadium": team["stadium"],
        "Avg. attendance": team["avg_attendance"],
    }
    display_dict(team_info)
