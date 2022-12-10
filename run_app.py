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
from st_aggrid.grid_options_builder import GridOptionsBuilder

from streamlit_app import instruction as instr
from streamlit_app import form as form
from streamlit_app import custom_display as cd
from streamlit_app import dashboard as dashboard


class Color:
    def __init__(self):
        self.RED = "#ED2E24"
        self.DARK_BLUE = "#052A5F"
        self.BLUE = "#0476BF"


COLOR = Color()

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
baseline_df = instr.get_baseline_df()
summary_df, raw_df = instr.get_ft_importance_df()

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


# process data
df_home = baseline_df[baseline_df["team2_name"] ==
                      input_params["home_team"].split(' (')[1].replace(')', '')]
df_home["date"] = pd.to_datetime(df_home["start_time"].apply(
    lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").date()))

# show attendance prediction (with comparison to avg attendance in previous years)
# _, col_1, _,  col_2, _ = st.columns([0.5, 1, 0.5, 1, 0.5])
st.markdown("### Attendance Prediction")

target_date, baseline_value = dashboard.get_baseline_value(
    df_home, input_params["date"], input_params["home_team"].split(' (')[1].replace(')', ''))  # type: ignore

metric_cols = st.columns([1 for _ in range(len(input_params['model']) + 1)])

for i, model in enumerate(input_params["model"]):
    with metric_cols[i]:
        cd.display_dial(title=f"[{model}] Attendance Prediction",
                        value="10,000", color=COLOR.BLUE, delta=-3000)

with metric_cols[-1]:
    # if "compare_year" not in st.session_state:
    #     st.session_state["compare_year"] = 2019
    # compare_year = st.slider("Year for comparison",
    #                          2015, 2019, 2019, 1, label_visibility="hidden")
    cd.display_dial(title=f"Moving Average 5-10 Attendance ({target_date.strftime('%A, %B %d, %Y')})",
                    value=f"{baseline_value:,.1f}", color=COLOR.DARK_BLUE)
    # st.session_state["compare_year"] = compare_year

# show MA 5-10 (this year)

st.markdown(f"### Moving Average 5-10 up till {processed_input['Date']}")


df_home_before = df_home[df_home["date"]
                         <= np.datetime64(input_params["date"])]
# moving average plot using a fake dataframe
ma_plt = dashboard.ma_chart(df_home_before, color=COLOR)  # type: ignore

st.altair_chart(ma_plt, use_container_width=True)


# show metrics of the selected model (MSE, RMSE, MAE, MAPE)


st.markdown("### Top Important Features")

# number of features to show for each model
num_of_features = st.slider("Number of features to show", 3, 10, 5, 1)

feature_cols = st.columns([1 for _ in range(len(input_params['model']))])

for i, model in enumerate(input_params["model"]):
    with feature_cols[i]:
        st.markdown(f"#### {model}")

        model_df = raw_df[raw_df["Model"] == model]
        if model_df.shape[0] == 0:
            st.warning(
                f"No feature importance data available for ***{model}*** model, please select another model for comparison.")
        else:
            ft_plt = dashboard.ft_imp_chart(  # type: ignore
                model_df, num_of_features, color=COLOR)  # type: ignore

            st.altair_chart(ft_plt, use_container_width=True)

with st.expander("🔢 Model Peformance", expanded=False):
    # aggrid bulder
    # streamlit table
    st.markdown("#### Model Feature Importance Summary Table")
    summary_df.rename(columns={'Unique Feature': 'Raw Feature Name',
                      'Processed Name': 'Feature Name', 'Occurrence': 'Occurrence across 5 Models'}, inplace=True)
    summary_df = summary_df[['Feature Name', 'Average Rank',
                             'Occurrence across 5 Models', 'Raw Feature Name']]
    gd = GridOptionsBuilder.from_dataframe(summary_df)
    gd.configure_pagination(
        enabled=True, paginationPageSize=10, paginationAutoPageSize=False)
    AgGrid(summary_df, gridOptions=gd.build(), height=300, width="100%")
    # top important features for each model

    st.markdown("#### Model Peformance Summary Table")
