import pandas as pd
import numpy as np
from pathlib import Path

RAW = Path(__file__).resolve().parents[1]/"data"/"PCOS_data.csv"
CLEANED = Path(__file__).resolve().parents[1]/"outputs"/"pcos_cleaned.csv"

def transform():
   
    df = pd.read_csv(RAW)
    print("Loaded raw data: ",RAW,"with shape: ",df.shape)

    df.columns = df.columns.str.strip()

    #handling null values for text datatypes cols
    for col in df.select_dtypes(include="object").columns:
        mode_val=df[col].mode()[0]
        df[col]=df[col].fillna(mode_val)

    #handling null values for numeric datatype cols
    for col in df.select_dtypes(include=[np.number]).columns:
        median_val=df[col].median()
        df[col]=df[col].fillna(median_val)

    df = df.drop(columns=["Hip(inch)","Waist:Hip Ratio",
    "TSH (mIU/L)", "AMH(ng/mL)", "PRL(ng/mL)", "PRG(ng/mL)", "RBS(mg/dl)",
    "BP _Systolic (mmHg)", "BP _Diastolic (mmHg)", "Follicle No. (L)", 
    "Follicle No. (R)", "Avg. F size (L) (mm)", "Avg. F size (R) (mm)", 
    "Endometrium (mm)", "Sl. No", "Patient File No.", "Pulse rate(bpm)", 
    "RR (breaths/min)", "Hb(g/dl)", "No. of abortions", "Unnamed: 44",
    "I   beta-HCG(mIU/mL)", "II    beta-HCG(mIU/mL)", "FSH(mIU/mL)","LH(mIU/mL)","FSH/LH"], errors="ignore")

    #feature engineering
    # 1-> irregular , 0 ->regular
    df["Cycle(R/I)"]=df["Cycle(R/I)"].replace({2:0,4:1,5:1})#check in notebook folder why this mapping was done

    df =df.rename(columns={
    "PCOS (Y/N)": "PCOS",
    "Age (yrs)": "Age",
    "Weight (Kg)": "Weight",
    "Height(Cm)": "Height",
    "BMI": "BMI",
    "Blood Group": "Blood_Group",
    "Cycle(R/I)": "Cycle_Type",
    "Cycle length(days)": "Menstrual_Days",
    "Marraige Status (Yrs)": "Marriage_Years",
    "Pregnant(Y/N)": "Pregnant",
    "Waist(inch)": "Waist",
    "Vit D3 (ng/mL)": "VitD3",
    "Weight gain(Y/N)": "Weight_Gain",
    "hair growth(Y/N)": "Hair_Growth",
    "Skin darkening (Y/N)": "Skin_Darkening",
    "Hair loss(Y/N)": "Hair_Loss",
    "Pimples(Y/N)": "Pimples",
    "Fast food (Y/N)": "Fast_Food",
    "Reg.Exercise(Y/N)": "Exercise"

   })
    #feature engineering
    corr=df.corr()["PCOS"].sort_values(ascending=False)#helps in finding which features are closely realted to pcos
    print(corr)
   
    df["bmi_category"]=pd.cut(df["BMI"],bins=[0,18.5,24.9,29.9,100],labels=["underweight","normal","overweight","obese"])

    #change name of cycle_length

    #save the clean dataset
    CLEANED.parent.mkdir(parents=True,exist_ok=True)#creates missing parent folder,& doesn't throw error if folder exists
    df.to_csv(CLEANED,index=False)#index=false->so that df index is not added as a separate col in csv
    print("\n Columns after cleaning: ",list(df.columns))
    print("\n First 5 rows: \n",df.head())
  
    
    return df
    #useful if you use transform() in another script

#calling as a standalone function
if __name__=="__main__":
    transform()

