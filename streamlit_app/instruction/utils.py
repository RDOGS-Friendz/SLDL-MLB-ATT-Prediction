import streamlit as st


def get_weather_list():
    weather_lst = ['Cloudy', 'Drizzle', 'In Dome', 'Overcast', 'Rain', 'Sunny']
    return weather_lst


@st.cache(ttl=60 * 60 * 24)
def get_model_list(baseline=False):
    if not baseline:
        model_list = [
            "Random Forest",
            "XGBoost",
            "LightGBM",
            "AdaBoost",
            "Stacking",
            "SVM"
        ]
    else:
        model_list = [
            'Average', 'Moving Average for most recent 5 games', 'Moving Average for past 5 - 10 games'
        ]

    return model_list


@st.cache(ttl=60 * 60 * 24)
def get_team_dict(type="all"):
    # Get all MLB team name list
    full_team_dict = {
        # abbr: full name
        "ARI": "Arizona Diamondbacks",
        "ATL": "Atlanta Braves",
        "BAL": "Baltimore Orioles",
        "BOS": "Boston Red Sox",
        "CHC": "Chicago Cubs",
        "CWS": "Chicago White Sox",
        "CIN": "Cincinnati Reds",
        "CLE": "Cleveland Indians",
        "COL": "Colorado Rockies",
        "DET": "Detroit Tigers",
        "HOU": "Houston Astros",
        "KC": "Kansas City Royals",
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
        "SD": "San Diego Padres",
        "SF": "San Francisco Giants",
        "SEA": "Seattle Mariners",
        "STL": "St. Louis Cardinals",
        "TB": "Tampa Bay Rays",
        "TEX": "Texas Rangers",
        "TOR": "Toronto Blue Jays",
        "WSH": "Washington Nationals",
    }

    full_team_stadium_dict = {
        # abbr: stadium name
        "ARI": "Chase Field",
        "ATL": "Truist Park",
        "BAL": "Oriole Park at Camden Yards",
        "BOS": "Fenway Park",
        "CHC": "Wrigley Field",
        "CWS": "Guaranteed Rate Field",
        "CIN": "Great American Ball Park",
        "CLE": "Progressive Field",
        "COL": "Coors Field",
        "DET": "Comerica Park",
        "HOU": "Minute Maid Park",
        "KC": "Kauffman Stadium",
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
        "SD": "Petco Park",
        "SF": "Oracle Park",
        "SEA": "T-Mobile Park",
        "STL": "Busch Stadium",
        "TB": "Tropicana Field",
        "TEX": "Globe Life Field",
        "TOR": "Rogers Centre",
        "WSH": "Nationals Park",
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
        ### How to use this app
        lorem ipsum dolor sit amet 
        """
    )

    st.markdown("")

    st.markdown(
        """
        ### How to interpret the results
        lorem ipsum dolor sit amet
        """
    )

    st.markdown("")

    st.markdown(
        """
        ### Behind the scenes
        lorem ipsum dolor sit amet
        """
    )

    st.markdown("")
    st.markdown(
        """
        ### References
        To try this app in Streamlit Sharing, you need to add your Twitter API credentials in the Secrets manager:
        1.  Go to your app dashboard at `https://share.streamlit.io/`
        2.  Find your app and click on `Edit secrets`:
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
