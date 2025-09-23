import streamlit as st
import requests

st.set_page_config(page_title="PCOS PATIENT DASHBOARD",page_icon="🩺",layout="centered")#tab_name kinda

#data_testid -> components of streamlit UI
page_bg="""
<style>
[data-testid="stAppViewContainer"]{
  background-color:#ffe6f0;

}
[data-testid="stHeader"]{
  background-color:#ff99cc;

}
[data-testid="stSidebar"]{
  background-color:#ffccdd;

}


</style>


"""

st.markdown(page_bg,unsafe_allow_html=True)#allows to use css/html 

st.title("💖 PCOS Prediction Dashboard")
st.markdown("Enter the following details for the patient:")

with st.form("pcos_form"):
    col1,col2=st.columns(2)#dividing page into 2 columns

    with col1:
        age = st.number_input("Age (years)",min_value=10,max_value=60,step=1)
        cycle_length = st.number_input("Cycle Length(Days)",min_value=0,max_value=20,step=1)
        weight = st.number_input("Weight (kg)")
        waist = st.number_input("Waist (inch)")
        bmi = st.number_input("BMI")
        marriage_yrs = st.number_input("Marriage Years",min_value=0.0,step=1.0)
    
    with col2:
        #format_func ->converts a number val to text,lambda->a shortcut way to define function
        skin_darkening=st.radio("Skin Darkening",[0,1],format_func=lambda x: "Yes" if x==1 else "No")
        hair_growth = st.radio("Hair Growth", [0,1], format_func=lambda x: "Yes" if x==1 else "No")
        weight_gain = st.radio("Weight Gain", [0,1], format_func=lambda x: "Yes" if x==1 else "No")
        cycle_type = st.radio("Cycle Type", [0,1], format_func=lambda x: "Irregular" if x==1 else "Regular")
        fast_food = st.radio("Fast Food", [0,1], format_func=lambda x: "Yes" if x==1 else "No")
        pimples = st.radio("Pimples", [0,1], format_func=lambda x: "Yes" if x==1 else "No")
        hair_loss = st.radio("Hair Loss", [0,1], format_func=lambda x: "Yes" if x==1 else "No")
   
    submitted = st.form_submit_button("Predict PCOS")

if submitted:
    data={
        "age": age,
        "cycle_length": cycle_length,
        "weight": weight,
        "waist": waist,
        "bmi": bmi,
        "skin_darkening": skin_darkening,
        "hair_growth": hair_growth,
        "weight_gain": weight_gain,
        "cycle_type": cycle_type,
        "fast_food": fast_food,
        "pimples": pimples,
        "hair_loss": hair_loss,
        "marriage_yrs": marriage_yrs

    }
    response = requests.post("http://127.0.0.1:8000/predict",json=data)

    if response.status_code == 200:
        result = response.json()
        if result["prediction"]==1:
            st.error(f"{result['message']}PCOS Probability:{result['probability_pcos']*100:.1f}%")
        else:
            st.success(f"{result['message']}PCOS Probability:{result['probability_pcos']*100:.1f}%")
    else:
        st.error("API Error : Could not connect to backend")



       
