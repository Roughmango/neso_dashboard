import streamlit as st

st.title("Introduction")
st.header("Live Overview")
st.write("The purpose of this page is to show you the current most recent data that has been taken from the api on carbon intensity")
st.write("It shows the forecast, actual and intensity index of the National carbon intensity, as well as for each region")

st.header("Forecast Accuracy")
st.write("This page revolves around the prediction model that has been created to try and better predict carbon intensity then the model featured in the api data."
         "It compares the mae and rmse of the api prediction model to the model that has been created and also shows how they compare to the actual value")

st.header("Generation mix")
st.write("This shows you the live fuel generation mix that has been taken from the api data for the nation and each region")

st.header("Smart advisor")
st.write("This page predicts the carbon intensity for each region in the next 24 hours and predicts which areas will have the lowest amount")