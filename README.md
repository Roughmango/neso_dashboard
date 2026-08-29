Website URL: https://addashboard-n8qf338l3bguvofoyy9chq.streamlit.app/

NESO Carbon Intensity Dashboard

A streamlit dashboard that has a persistent, automated, automated,end to end data system around a live API. It has various features related to the UK electricity carbon intensity, generation mix and its accuracy. The dashboard uses data from the NESO carbon intensity API and provides both live visualization
and machine learning based predictions to help identify periods and regions that will have the lowest carbon intensity in a future period.
Automated scheduled ingestion of live API data using GitHub Actions makes sure data is always up to date.

Features:
POSTGRESQL database with a size 6000 records when readme last updated with more automatically added every half an hour.

The Live Overview Page: The purpose of this page is to show you the current most recent data that has been taken from the API on carbon intensity
It shows the forecast, actual and intensity index of the National carbon intensity, as well as for each region

The Forecast Accuracy Page: This page revolves around the prediction model that has been created to try and better predict carbon intensity then the model featured in the api data.
It compares the mae and rmse of the api prediction model to the model that has been created and also shows how they compare to the actual value.

The Generation Mix Page: This shows you the live fuel generation mix that has been taken from the API data for the nation and each region

The Smart Advisor Page: This page predicts the carbon intensity for each region in the next 24 hours and predicts which areas will have the lowest amount


Machine learning:
The project uses XGBoost for carbon-intensity prediction.

The model uses features including:

Forecast carbon intensity
Hour and minute
Day of week
Weekend indicator
Time of day
Recent intensity changes
Previous intensity values
Same-period-previous-day intensity
Rolling intensity averages
Previous forecast errors
Rolling forecast errors
Renewable generation
Fossil generation
Low-carbon generation

Data Pipeline

The project follows a general pipeline of:

NESO API

↓
Data collection
   ↓
Transformation / validation
   ↓
Database
   ↓
Data access layer
   ↓
Streamlit dashboard
   ↓
Visualisations + ML predictions

The repository includes scripts for fetching, transforming and validating the data, alongside a database schema.

Technologies

The project is built using:

Python
Streamlit
Pandas
XGBoost
Scikit-learn
Plotly
SQLAlchemy
PostgreSQL
Python-dotenv

The required Python dependencies are listed in requirements.txt.

Project goals

Create my own public database, automating the addition of data to it from the API.
Analyse how accurate the original model is.
Create my own purpose built model to improve the carbon intensity forecast
Create my own web page to display my findings and model.
Turn the model into something that can be used to find out predictions for the future.

This project was an exercise in building a realistic end to end pipeline. It had scheduled data 
collection from a live public API,an append-only storage design that 
preserves forecast revisions over time, a machine learning model created specifically to improve predictions and a deployed, interactive front end — rather than a one-off analysis of a static dataset.
