import datetime
import pandas as pd
import numpy as np
import streamlit as st
import time
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

from streamlit_app import instruction as instr
from streamlit_app import form as form
from streamlit_app import custom_display as cd
from streamlit_app import dashboard as dashboard
from streamlit_app import model as mdl


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
baseline_df = instr.get_baseline_df()  # raw test set
summary_df, raw_df = instr.get_ft_importance_df()
model_pf_df = instr.get_model_pf_df()

input_params = form.create_form(team_lst=team_lst, weather_lst=weather_lst,
                                model_lst=model_lst, baseline_model_lst=baseline_model_lst)

# --------------------------------------------------------------------------------------------------
# process input
# process data
df_home = baseline_df[baseline_df["team2_name"] ==
                      input_params["home_team"]]
df_home["date"] = pd.to_datetime(df_home["start_time"].apply(
    lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").date()))


# show attendance prediction (with comparison to avg attendance in previous years)
# _, col_1, _,  col_2, _ = st.columns([0.5, 1, 0.5, 1, 0.5])

target_date, baseline_value, real_value = dashboard.get_baseline_value(
    df_home, input_params["date"], input_params["home_team"])  # type: ignore

# processed dict
if target_date == input_params["date"]:
    processed_input = {"Date": input_params["date"].strftime("%A, %B %d, %Y"),
                       "Start Hour": input_params["start_hour"],
                       "Playoff": input_params["season_type"],
                       "Home Team": f'{team_dict[input_params["home_team"]]} ({input_params["home_team"]})',
                       "Away Team": f'{team_dict[input_params["away_team"]]} ({input_params["away_team"]})',
                       "Weather": input_params["weather"],
                       "Temperature": input_params["temperature"],
                       "Actual Attendance": f'{real_value:,} ppl',
                       "Model": input_params["model"]}
else:
    processed_input = {"Date": input_params["date"].strftime("%A, %B %d, %Y"),
                       "Nearest Game Date": target_date.strftime("%A, %B %d, %Y"),
                       "Start Hour": input_params["start_hour"],
                       "Playoff": input_params["season_type"],
                       "Home Team": f'{team_dict[input_params["home_team"]]} ({input_params["home_team"]})',
                       "Away Team": f'{team_dict[input_params["away_team"]]} ({input_params["away_team"]})',
                       "Weather": input_params["weather"],
                       "Temperature": input_params["temperature"],
                       "Actual Attendance": f'{real_value:,} ppl',
                       "Model": input_params["model"]}

# model input
_model_input = mdl.streamlit_to_model(input_params)  # type: ignore

# --------------------------------------------------------------------------------------------------
# Draw results

st.markdown(
    f"## Dashboard")


with st.expander("ℹ Game Information (Input Params)", expanded=True):
    cd.display_dict(processed_input)

st.markdown("### Attendance Prediction")

metric_cols = st.columns([1 for _ in range(len(input_params['model']) + 1)])

for i, model in enumerate(input_params["model"]):
    with metric_cols[i]:
        # make sure that the model has the str type
        _tmp_model = mdl.Model(str(model))
        val = _tmp_model.predict(_model_input)[0]
        delta = val - real_value

        cd.display_dial(title=f"[{model}] Attendance Prediction",
                        value=f'{val:,.2f}', color=COLOR.BLUE, delta=delta)

with metric_cols[-1]:
    # if "compare_year" not in st.session_state:
    #     st.session_state["compare_year"] = 2019
    # compare_year = st.slider("Year for comparison",
    #                          2015, 2019, 2019, 1, label_visibility="hidden")

    delta = baseline_value - real_value  # type: ignore

    cd.display_dial(title=f"Moving Average 5-10 Attendance ({target_date.strftime('%A, %B %d, %Y')})",
                    value=f"{baseline_value:,.2f}", color=COLOR.DARK_BLUE, delta=delta)
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

    # st.write(model_pf_df.columns)
    gd = GridOptionsBuilder.from_dataframe(model_pf_df)
    gd.configure_pagination(
        enabled=False, paginationPageSize=10, paginationAutoPageSize=False)
    # select box
    gd.configure_column(field="Params",
                        wrapText=True, autoHeight=True, cellStyle={'wordBreak': 'normal'}, width=300)

    AgGrid(model_pf_df, gridOptions=gd.build(), height=300,
           width="100%")
