import streamlit as st
import pandas as pd
import datetime


def get_weather_list():
    weather_lst = ['Cloudy', 'Drizzle', 'In Dome', 'Overcast', 'Rain', 'Sunny']
    return weather_lst


@st.cache(ttl=60 * 60 * 24)
def get_baseline_df():
    path = 'model/testset_w_lle.csv'
    df = pd.read_csv(path)

    return df


@st.cache(ttl=60 * 60 * 24)
def get_ft_importance_df():
    path = 'streamlit_app/instruction/model_feature_importance.xlsx'
    summary_df = pd.read_excel(path, sheet_name='Summary', engine='openpyxl')
    raw_df = pd.read_excel(
        path, sheet_name='Ft. Importance Table', engine='openpyxl')

    return summary_df, raw_df


@st.cache(ttl=60 * 60 * 24, allow_output_mutation=True)
def get_model_pf_df():
    # model performance table
    path = 'streamlit_app/instruction/model_perf_summary.xlsx'
    df = pd.read_excel(path, engine='openpyxl').drop(
        columns=['Description'], axis=1)

    return df


@st.cache(ttl=60 * 60 * 24)
def get_model_list(baseline=False):
    if not baseline:
        model_list = [
            "XGBoost",
            "Stacking",
            "Ridge",
            "Gradient Boosting",
            "SVM",
            "Deep Learning Regression"
        ]
    else:
        model_list = [
            'Average', 'Moving Average for most recent 5 games', 'Moving Average for past 5 - 10 games'
        ]

    return model_list


@st.cache(ttl=60 * 60 * 24)
def get_team_dict(type="all"):

    # team_list = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'LAA', 'LAD',
    #              'MIA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'STL', 'TBR', 'TEX', 'TOR', 'WSN']

    # Get all MLB team name list
    full_team_dict = {
        # abbr: full name
        "ARI": "Arizona Diamondbacks",
        "ATL": "Atlanta Braves",
        "BAL": "Baltimore Orioles",
        "BOS": "Boston Red Sox",
        "CHC": "Chicago Cubs",
        "CHW": "Chicago White Sox",
        "CIN": "Cincinnati Reds",
        "CLE": "Cleveland Indians",
        "COL": "Colorado Rockies",
        "DET": "Detroit Tigers",
        "HOU": "Houston Astros",
        "KCR": "Kansas City Royals",
        "LAA": "Los Angeles Angels",
        "LAD": "Los Angeles Dodgers",
        "MIA": "Miami Marlins",
        "MIL": "Milwaukee Brewers",
        "MIN": "Minnesota Twins",
        "NYM": "New York Mets",
        "NYY": "New York Yankees",
        "OAK": "Oakland Athletics",
        "PHI": "Philadelphia Phillies",
        "PIT": "Pittsburgh Pirates",
        "SDP": "San Diego Padres",
        "SEA": "Seattle Mariners",
        "SFG": "San Francisco Giants",
        "STL": "St. Louis Cardinals",
        "TBR": "Tampa Bay Rays",
        "TEX": "Texas Rangers",
        "TOR": "Toronto Blue Jays",
        "WSN": "Washington Nationals",
    }

    full_team_stadium_dict = {
        # abbr: stadium name
        "ARI": "Chase Field",
        "ATL": "Truist Park",
        "BAL": "Oriole Park at Camden Yards",
        "BOS": "Fenway Park",
        "CHC": "Wrigley Field",
        "CHW": "Guaranteed Rate Field",
        "CIN": "Great American Ball Park",
        "CLE": "Progressive Field",
        "COL": "Coors Field",
        "DET": "Comerica Park",
        "HOU": "Minute Maid Park",
        "KCR": "Kauffman Stadium",
        "LAA": "Angel Stadium of Anaheim",
        "LAD": "Dodger Stadium",
        "MIA": "Marlins Park",
        "MIL": "Miller Park",
        "MIN": "Target Field",
        "NYM": "Citi Field",
        "NYY": "Yankee Stadium",
        "OAK": "Oakland Coliseum",
        "PHI": "Citizens Bank Park",
        "PIT": "PNC Park",
        "SDP": "Petco Park",
        "SFG": "Oracle Park",
        "SEA": "T-Mobile Park",
        "STL": "Busch Stadium",
        "TBR": "Tropicana Field",
        "TEX": "Globe Life Field",
        "TOR": "Rogers Centre",
        "WSN": "Nationals Park",
    }

    if type == "abbr:stadium":
        return full_team_stadium_dict
    elif type == "abbr:full":
        return full_team_dict
    else:

        detailed_stadium_dict = {}
        for abbr, full_name in full_team_dict.items():
            detailed_stadium_dict[abbr] = {
                "full_name": full_name,
                "stadium_name": full_team_stadium_dict[abbr],
            }

        return detailed_stadium_dict


def create_usage_instruction():
    """Create a description of the instructions."""
    st.markdown(
        """
        ### Our Models

        - Models includes Lasso, Ridge, Gradient Boosting, Bagging, SVM, and XGBoost
        - After training above models, we choose 3~5 models with best parameters to do stacking
        - We use 5-fold cross validation to ensure model robustness and avoid overfitting
        """
    )

    st.markdown("")

    st.markdown(
        """
        ### Evaluation Metrics
        
        - MSE
        - RMSE
        - MAE
        - MAPE
        """
    )

    st.markdown("")

    st.markdown(
        """
        ### How We Build the Models
        
        1. 5-fold on training set
        2. Find the best hyper parameters
        3. 5-fold as the final training set, re-train with the best hyper parameters
        4. Save model
        5. Measure the performance on the test set
        """
    )

    st.markdown("")
    return


def create_header():
    a, b = st.columns([1, 6])

    with a:
        st.text("")
        st.image("assets/Major_League_Baseball_logo.svg.png", width=100)
    with b:
        st.title("MLB Attendance Predictor")

    st.write("Please fill in or select the following information to predict the attendance of a 2022 MLB game. Enjoy!")
    return
