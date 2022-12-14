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

```
📦report
 ┣ 📂data
 ┃ ┣ 📂baseball-reference
 ┃ ┗ 📂players
 ┣ 📂data-collection
 ┃ ┣ 📜data_exploration.html
 ┃ ┣ 📜data_exploration.ipynb
 ┃ ┣ 📜descriptive_statistics.html
 ┃ ┣ 📜descriptive_statistics.ipynb
 ┃ ┣ 📜sportsdataio.html
 ┃ ┣ 📜sportsdataio.ipynb
 ┃ ┣ 📜web_scrapping.html
 ┃ ┗ 📜web_scrapping.ipynb
 ┣ 📂data-engineering
 ┃ ┣ 📜data_cleaning.html
 ┃ ┣ 📜data_cleaning.ipynb
 ┃ ┣ 📜dimension_reduction.html
 ┃ ┗ 📜dimension_reduction.ipynb
 ┣ 📂model-v1
 ┃ ┣ 📜statistical_learning.html
 ┃ ┗ 📜statistical-learning.ipynb
 ┣ 📂model-v2
 ┃ ┣ 📜deep-learning.html
 ┃ ┣ 📜deep-learning.ipynb
 ┃ ┣ 📜statistical_learning_model.html
 ┃ ┣ 📜statistical_learning_model.ipynb
 ┣ 📂streamlit
 ┃ ┣ 📂model
 ┃ ┣ 📂streamlit_app
 ┃ ┗ 📜run_app.py
 ┃ 📜presentation.pdf
 ┃ 📜presentation.mp4
 ┗ 📜README.md
```

## Data Collection
### [Web scraping](data-collection/web_scrapping.ipynb)
In this section, we collect data from [baseball reference](https://www.baseball-reference.com/).

### [API](data-collection/sportsdataio.ipynb)
In this section, we collect data from [sportsdataio](https://sportsdata.io/).

### [Descrptive Statistics](data-collection/descriptive_statistics.ipynb) & [Data Exploration](data-collection/data_exploration.ipynb)
In this section, we analyze data we collected, find out the potential important factor and seek what data engineering we can do.


## Data Engineering
### [Data Cleaning & Processing](data-engineering/data_cleaning.ipynb)
In this section, we clean the date we collected, perform one-hot encoding on forecast weather, team players, home team, away team, season type, month and venue. And then generate some features such as weekday, start_hour, is_holiday, team's history winning rate, winning streak, etc.

As to player data, we select players whose salary over 5 millinos and belong to all star.

### [Dimension Reduction](data-engineering/dimension_reduction.ipynb)
In this section, we want reduce players dimension. We try all kinds of dimension reduction method and found that LLE performs best. 

## Model Building v1
### [Statistical Learning Model](model-v1/statistical-learning.ipynb)
In this section, we build our model with original data processed at [data cleaning section](#data-cleaning--processing). Model includes KNN, lasso, ridge, decision tree, gradient boosting, adaboost, bagging, svm, and XGBoost. To avoid overfitting and enhance model robustness, we use 5-fold cross validation to find out the best parameters. After that, we train the model with all training set and then evaluate testing set with MSE, RMSE, MAE, MAPE.

## Model Building v2
### [Statistical Learning Model](model-v2/statistical_learning_model.ipynb)
In this section, we build our model with data processed after [dimension reduction](#dimension-reduction). Model includes lasso, ridge, gradient boosting, bagging, svm, and XGBoost. To avoid overfitting and enhance model robustness, we use 5-fold cross validation to find out the best parameters. After that, we train the model with all training set and then evaluate testing set with MSE, RMSE, MAE, MAPE.

After building above models, we choose 3~5 models with best performance at validation set to do stacking.

### [Deep Learning Model](model-v2/deep-learning.ipynb)
In this section, we build deep learning model with data processed after [dimension reduction](#dimension-reduction).

## Streamlit
In this section, we deploy a prediction website with [model v2](#model-building-v2). The link is [https://mlb-att-pred.streamlit.app](https://mlb-att-pred.streamlit.app)

### Run locally
1. `cd streamlit`
2. `pip install -r requirements.txt`
3. `streamlit run run_app.py`

## Conclusion
1. The best RMSE is 6004, XGBoost model.
2. The best MAPE is 0.2302, Ridge regression.
3. Stacking model considers various models, and the result is pretty good.
4. Teams, players, stadium, weekday are actually the most important factor to predict attendance number.
5. Our model outperformed baseline(simple moving average) by 10% MAPE

## Future Work
1. Improve model predict ability
2. There may still be features that are important but have not been included in our models
3. Our work can be further applied to CPBL, contributing to Taiwanese baseball league and fans!
