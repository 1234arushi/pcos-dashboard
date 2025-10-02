from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import joblib
import os
from pathlib import Path
from sqlalchemy import create_engine,Table,Column,Integer,Float,String,MetaData,select
import pandas as pd  # ✅ added to build DataFrame with correct column order

MODEL_PATH = Path(__file__).resolve().parents[0]/"models"/"pcos_model.pkl"
model = joblib.load(MODEL_PATH)

app = FastAPI(title = "PCOS Prediction API")

load_dotenv()#load variables from .env

#reading db details
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

#build connection string for sqlAlchemy
CONN_STR = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(CONN_STR)
metadata = MetaData()

# Table for storing patient predictions
patients_predictions = Table(
    "patients_predictions",metadata,
    Column("id",Integer,primary_key = True,autoincrement = True),
    Column("patient_id", String ,unique=True),
    Column("name", String),
    Column("age", Integer),
    Column("menstrual_days", Integer),
    Column("weight", Float),
    Column("waist", Float),
    Column("bmi", Float),
    Column("skin_darkening", Integer),
    Column("hair_growth", Integer),
    Column("weight_gain", Integer),
    Column("cycle_type", Integer),
    Column("fast_food", Float),
    Column("pimples", Integer),
    Column("hair_loss", Integer),
    Column("marriage_yrs", Float),
    Column("prediction", Integer)
)
metadata.create_all(engine)#creates if not exists

# Schema for doctor input
class PatientInput(BaseModel):#used when we get request from doctor in json
    age : int
    menstrual_days : int
    weight : float
    waist : float
    bmi : float
    skin_darkening:int
    hair_growth : int
    weight_gain : int
    cycle_type : int
    fast_food : float
    pimples : int
    hair_loss : int
    marriage_yrs : float
    name : str

@app.post("/predict")#when request made to this handle,then call below function
def predict(input : PatientInput):
    # Use the same column order as training (selected_features)
    #step 1:imp
    selected_features = [
        "Skin_Darkening","Hair_Growth","Weight_Gain","Cycle_Type",
        "Fast_Food","Pimples","Weight","BMI","Hair_Loss","Waist",
        "Age","Menstrual_Days","Marriage_Years"
    ]

    #features have to be 2-d array with same order as training
    #step 2:imp
    features_df = pd.DataFrame([[
        input.skin_darkening,
        input.hair_growth,
        input.weight_gain,
        input.cycle_type,
        input.fast_food,
        input.pimples,
        input.weight,
        input.bmi,
        input.hair_loss,
        input.waist,
        input.age,
        input.menstrual_days,
        input.marriage_yrs
    ]], columns=selected_features)

    #default -> predict_proba returns [[P(0),P(1)]]->select prob for PCOS=1
    proba = float(model.predict_proba(features_df)[:,1][0])
    threshold = 0.4
    pred = 1 if proba >= threshold else 0

    patient_id = f"{input.age}_{input.name.lower()}"

    with engine.begin() as conn:
        # . c -> to access columns by name
        existing = conn.execute(
            select(patients_predictions)
            .where(patients_predictions.c.patient_id == patient_id)
        ).first()

        if existing:
            
            conn.execute(
                patients_predictions.update()
                .where(patients_predictions.c.patient_id == patient_id)
                .values(
                    age=input.age,
                    name=input.name,
                    menstrual_days=input.menstrual_days,
                    weight=input.weight,
                    waist=input.waist,
                    bmi=input.bmi,
                    skin_darkening=input.skin_darkening,
                    hair_growth=input.hair_growth,
                    weight_gain=input.weight_gain,
                    cycle_type=input.cycle_type,
                    fast_food=input.fast_food,
                    pimples=input.pimples,
                    hair_loss=input.hair_loss,
                    marriage_yrs=input.marriage_yrs,
                    prediction=pred
                )
            )
        else:
         
            conn.execute(
                patients_predictions.insert().values(
                    patient_id=patient_id,
                    name=input.name,
                    skin_darkening=input.skin_darkening,
                    hair_growth=input.hair_growth,
                    weight_gain=input.weight_gain,
                    cycle_type=input.cycle_type,
                    fast_food=input.fast_food,
                    pimples=input.pimples,
                    weight=input.weight,
                    bmi=input.bmi,
                    hair_loss=input.hair_loss,
                    waist=input.waist,
                    age=input.age,
                    menstrual_days=input.menstrual_days,
                    marriage_yrs=input.marriage_yrs,
                    prediction=pred
                )
            )

    return {
        "prediction": pred,
        "probability_pcos": round(proba, 2),
        "message": "You have PCOS with " if pred == 1 else "No, you don't have PCOS with "
    }

@app.get("/patients")
def get_patients():
    with engine.connect() as conn:#engine.connect() -> is for read_only queries
        res = conn.execute(select(patients_predictions))
        rows = [dict(r._mapping)for r in res]#returned as json
    return {"patients":rows}
