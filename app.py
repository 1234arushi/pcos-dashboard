import streamlit as st#this makes our web app
import pandas as pd# this helps us work with data

# for title of dashboard
st.title("PCOS Dashboard")

# uploading a csv file
file = st.file_uploader("Upload PCOS dataset",type="csv")

if file:
    # read the file into a table(=dataframe)
    df=pd.read_csv(file)
    st.write("Here is your data")
    # show first 5 rows
    st.write(df.head()) 
