import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import _pickle as cPickle


def GetMetaGameInfo(html):
    soup = BeautifulSoup(html, "html.parser")
    scorebox = soup.find("div", {"class": "scorebox"})
    t1, t2, score_box_meta = (list(scorebox.children)[i] for i in [1,3,5])
    for t in [t1, t2]:
        t.name = t.find("strong").text.strip(" ").strip("\n").replace(" ", "").replace(".", "")
        t.score = int(t.find("div", {"class": "score"}).text)
        t.pre_win, t.pre_loss = (int(i) for i in list(t.children)[4].text.split('-'))
    if t1.score > t2.score:
        t1.pre_win -= 1
        t2.pre_loss -= 1
    else:
        t2.pre_win -= 1
        t1.pre_loss -= 1
    date, start_time, att, venue, duration, at_night_on_grass = list(list(score_box_meta.children)[i].text for i in [1, 2, 3, 4, 5, 6] )
    have_att = "Attendance" in att
    at_night = None
    on_grass = None
    if have_att:
        date = datetime.strptime(date, "%A, %B %d, %Y")
        start_time = datetime.strptime("".join(start_time.split(" ")[2:4]).replace(".", ""), "%I:%M%p")
        start_time = date + timedelta(hours=start_time.hour, minutes=start_time.minute)
        duration = datetime.strptime(duration[15:], "%H:%M")
        duration = timedelta(hours=duration.hour, minutes=duration.minute)
        at_night, on_grass = at_night_on_grass.split(", ")
        at_night = 'Night Game' == at_night
        on_grass = 'on grass' == on_grass
        att = int(att.split(": ")[1].replace(",", ""))
        venue = venue.split(": ")[1]    
    gameInfo = {
        "have_att": have_att,
        "start_time": start_time, "duration": duration,
        "venue": venue, "at_night": at_night, "on_grass": on_grass,
        "att": att
    }
    return t1, t2, gameInfo

# soup = BeautifulSoup(, "html.parser")
def GetTable(html, table_id):
    soup = BeautifulSoup(html, "html.parser")
    tbody = soup.find("div", {"id": table_id}).find("tbody")
    table = []
    for tr in tbody.findAll("tr"):
        row = []
        name = tr.find("th").text
        row.append(name)
        for td in tr.findAll("td"):
            row.append(td.text)
        if not all([i == "" for i in row]):
            table.append(row)
    return pd.DataFrame(table, columns=[
        'Batting',
        'AB',
        'R',
        'H',
        'RBI',
        'BB',
        'SO',
        'PA',
        'BA',
        'OBP',
        'SLG',
        'OPS',
        'Pit',
        'Str',
        'WPA',
        'aLI',
        'WPA+',
        'WPA-',
        'cWPA',
        'acLI',
        'RE24',
        'PO',
        'A',
        'Details'
    ])
    
def setup_driver():
    options = Options()
    options.headless = False

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(
    ).install()), options=options)
    driver.set_page_load_timeout(5)
    return driver

def scratch_meta_page():
    url = "https://www.baseball-reference.com/leagues/majors/2021-schedule.shtml"
    driver = setup_driver()
    
    while True:
        try:
            driver.get(url)
        except TimeoutException:
            print("load page timeout")

        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "game")))
        except TimeoutException:
            continue
        break
    print("get meta data")
    return driver.page_source


def scratch_single_page(url):
    print(f"Scratch {url}")
    driver=setup_driver()

    # load page for 4 sec
    try:
        driver.get(url)
    except TimeoutException:
        print("load page timeout")

    team1, team2, metaGameInfo = GetMetaGameInfo(driver.page_source)
    df1=GetTable(driver.page_source, f"all_{team1.name}batting")
    df2=GetTable(driver.page_source, f"all_{team2.name}batting")
    print("get page data success")
    
    team1={
        "name": team1.name,
        "pre_win": team1.pre_win,
        "pre_loss": team1.pre_loss,
        "player_df": df1
    }
    team2={
        "name": team2.name,
        "pre_win": team2.pre_win,
        "pre_loss": team2.pre_loss,
        "player_df": df2
    }

    gameInfo={
        "meta_game_info": metaGameInfo,
        "team1": team1,
        "team2": team2
    }

    return gameInfo


# from the index page get all game url
html = scratch_meta_page()
soup = BeautifulSoup(html, "html.parser")
games = soup.findAll("p", {"class": "game"})

data = dict()
# load previous scratched games data
with open("gamesData.pickle", "rb") as output_file:
    data = cPickle.load(output_file)

# scratch the rest
for game in games:
    game_url = "https://www.baseball-reference.com" + game.find("em").find("a")['href']
    
    # ignore if already have data
    if game_url in data:
        continue
    #scratch game
    gameInfo = scratch_single_page(game_url)
    # save to data
    data[game_url] = gameInfo
    with open("gamesData.pickle", "wb") as output_file:
        cPickle.dump(data, output_file)