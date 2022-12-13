<h1 align="center">
  MLB Attendance Prediction
</h1>

<h3 align="center">Official Documentation (with Instructions)</h3>
<h4 align="center">IM 5061 Final Project</h4>

<p align="center">
  <a href="https://mlb-att-pred.streamlit.app">
    Try to predict on our website
  </a>
</p>

## Table of Contents

📦report
 ┣ 📂data-collection
 ┃ ┗ 📜.gitkeep
 ┣ 📂data-engineering
 ┃ ┗ 📜.gitkeep
 ┣ 📂model-v1
 ┃ ┗ 📜.gitkeep
 ┣ 📂model-v2
 ┃ ┣ 📜.gitkeep
 ┃ ┣ 📜statistical_learning_model.html
 ┃ ┗ 📜statistical_learning_model.ipynb
 ┣ 📂streamlit
 ┃ ┗ 📜.gitkeep
 ┗ 📜README.md

## Data Collection
### [Web scraping]()
In this section, we collect data from [baseball reference](https://www.baseball-reference.com/).

### [API]()
In this section, we collect data from [sportsdataio](https://sportsdata.io/).

### [Descrptive Statistics]()
In this section, we analyze data we collected, find out the potential important factor and seek what data engineering we can do.

## Data Engineering
### [Data Cleaning & Processing]()
In this section, we clean the date we collected, perform one-hot encoding on forecast weather, team players, home team, away team, season type, month and venue. And then generate some features such as weekday, start_hour, is_holiday, team's history winning rate, winning streak, etc.

As to player data, we select players whose salary over 5 millinos and belong to all star.

### [Dimension Reduction]()
In this section, we want reduce players dimension. We try all kinds of dimension reduction method and found that LLE performs best. 

## Model Building v1
### [Statistical Learning Model]()
In this section, we build our model with original data processed at [data cleaning section](#data-cleaning--processing). Model includes KNN, lasso, ridge, decision tree, gradient boosting, adaboost, bagging, svm, and XGBoost. To avoid overfitting and enhance model robustness, we use 5-fold cross validation to find out the best parameters. After that, we train the model with all training set and then evaluate testing set with MSE, RMSE, MAE, MAPE.

## Model Building v2
### [Statistical Learning Model](model-v2/statistical_learning_model.ipynb)
In this section, we build our model with data processed after [dimension reduction](#dimension-reduction). Model includes lasso, ridge, gradient boosting, bagging, svm, and XGBoost. To avoid overfitting and enhance model robustness, we use 5-fold cross validation to find out the best parameters. After that, we train the model with all training set and then evaluate testing set with MSE, RMSE, MAE, MAPE.

After building above models, we choose 3~5 models with best performance at validation set to do stacking.

### [Deep Learning Model]()
In this section, we build deep learning model with data processed after [dimension reduction](#dimension-reduction).

## Streamlit
In this section, we deploy a prediction website with [model v2](#model-building-v2). The link is [https://mlb-att-pred.streamlit.app](https://mlb-att-pred.streamlit.app)

### Run locally
1. `cd streamlit`
2. `pip install -r requirements.txt`
3. `python run_app.py`
