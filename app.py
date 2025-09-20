import streamlit as st#this makes our web app
import pandas as pd# this helps us work with data

# for title of dashboard
st.title("PCOS Risk Checker 🩺")
st.write("Fill in the details below to check your estimated PCOS risk")

#user inputs
age=st.number_input("Age",min_value = 15,max_value=45,value=25)#value = 25->Default age
bmi=st.number_input("BMI(Body Mass Index)",min_value=10.0,max_value=50.0,value=22.5,step=0.01)
cycle_length=st.number_input("Cycle Length(days)",min_value=15,max_value=60,value=28)
hair_growth=st.selectbox("Excess Hair Growth",["No","Yes"])
acne=st.selectbox("Acne",["No","Yes"])
sleep_hours=st.number_input("Average Sleep(hours/day)",min_value=3,max_value=12,value=7)

#demo logic
risk_score = 0
if bmi > 25 :
    risk_score+=20
if cycle_length > 35:
    risk_score+=30
if hair_growth == "Yes":
    risk_score+=20
if acne == "Yes":
    risk_score+=15
if sleep_hours < 6 :
    risk_score+=15
risk_score=min(risk_score,100)

if risk_score < 30:
    st.success("Low Risk ; Maintain healthy lifestyle")
elif risk_score < 60 :
    st.warning("Moderate Risk ; Consider consulting a doctor")
else:
    st.error("High Risk ; Please seek medical advice")

