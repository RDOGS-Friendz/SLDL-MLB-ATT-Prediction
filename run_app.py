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
import plotly.express as px
import altair as alt
from vega_datasets import data
from st_aggrid import AgGrid

from streamlit_app import instruction as instr
from streamlit_app import form as form
from streamlit_app import custom_display as cd

COLOR_RED = "#ED2E24"
COLOR_DARK_BLUE = "#052A5F"
COLOR_BLUE = "#0476BF"


st.set_page_config(page_icon="⚾", page_title="MLB Attendance Predictor")

st.write('<base target="_blank">', unsafe_allow_html=True)

prev_time = [time.time()]

instr.create_header()

with st.expander("ℹ️ About", expanded=False):
    instr.create_usage_instruction()

st.write("")


team_dict = instr.get_team_dict(type="abbr:full")
team_lst = sorted(list([f'{v} ({k})' for k, v in team_dict.items()]))
stadium_lst = list(instr.get_team_dict(type="abbr:stadium").values())
weather_lst = list(instr.get_weather_list())
model_lst = instr.get_model_list()
baseline_model_lst = instr.get_model_list(True)

input_params = form.create_form(team_lst=team_lst, weather_lst=weather_lst,
                                model_lst=model_lst, baseline_model_lst=baseline_model_lst)

# --------------------------------------------------------------------------------------------------
# process input

# processed dict
processed_input = {"Date": input_params["date"].strftime("%A, %B %d, %Y"),
                   "Start Hour": input_params["time"],
                   "Playoff": input_params["season_type"],
                   "Home Team": input_params["home_team"],
                   "Away Team": input_params["away_team"],
                   "Weather": input_params["weather"],
                   "Temperature": input_params["temperature"], "Model": input_params["model"]}

# read models

# --------------------------------------------------------------------------------------------------
# Draw results

st.markdown(
    f"## Dashboard")


with st.expander("ℹ Input Parameters Information", expanded=True):
    cd.display_dict(processed_input)


# {input_params['home_team']} vs. {input_params['away_team']} @ {input_params['stadium']} on {input_params['date'].strftime('%A, %B %d, %Y')}", unsafe_allow_html=True)

# st.write(input_params)

# show attendance prediction (with comparison to avg attendance in previous years)
# _, col_1, _,  col_2, _ = st.columns([0.5, 1, 0.5, 1, 0.5])
st.markdown("### Attendance Prediction")

metric_cols = st.columns([1 for _ in range(len(input_params['model']) + 1)])

for i, model in enumerate(input_params["model"]):
    with metric_cols[i]:
        cd.display_dial(title=f"[{model}] Attendance Prediction",
                        value="10,000", color=COLOR_BLUE, delta=-3000)

with metric_cols[-1]:
    # if "compare_year" not in st.session_state:
    #     st.session_state["compare_year"] = 2019
    # compare_year = st.slider("Year for comparison",
    #                          2015, 2019, 2019, 1, label_visibility="hidden")
    cd.display_dial(title=f"Moving Average 5-10 Attendance",
                    value="10,000", color=COLOR_DARK_BLUE)
    # st.session_state["compare_year"] = compare_year

# show MA 5-10 (this year)

st.markdown(f"### Moving Average 5-10 up till {processed_input['Date']}")

# moving average plot using a fake dataframe
source = data.wheat()

bar = alt.Chart(source).mark_bar(color=COLOR_BLUE).encode(  # type: ignore
    x='year:O',
    y='wheat:Q',
    tooltip=['year', 'wheat']
)

line = alt.Chart(source).mark_line(color=COLOR_RED).transform_window(  # type: ignore
    # The field to average
    rolling_mean='mean(wheat)',
    # The number of values before and after the current value to include.
    frame=[-9, 0]
).encode(
    x='year:O',
    y='rolling_mean:Q',
    tooltip=['year']
)

tmp_plt = (bar + line).interactive()

st.altair_chart(tmp_plt, use_container_width=True)


# show metrics of the selected model (MSE, RMSE, MAE, MAPE)


st.markdown("### Top Important Features")

# number of features to show for each model
num_of_features = st.slider("Number of features to show", 3, 25, 10, 1)

feature_cols = st.columns([1 for _ in range(len(input_params['model']))])

for i, model in enumerate(input_params["model"]):
    with feature_cols[i]:
        st.markdown(f"#### {model}")
        source = data.barley()

        tmp_plt = alt.Chart(source).mark_bar(color=COLOR_BLUE).encode(  # type: ignore
            x='sum(yield):Q',
            y=alt.Y('site:N', sort='-x')  # type: ignore
        )

        st.altair_chart(tmp_plt, use_container_width=True)

with st.expander("🔢 Model Peformance", expanded=False):
    # streamlit table
    tmp_df = pd.read_csv(
        'https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
    AgGrid(tmp_df)
    # top important features for each model
