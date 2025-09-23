import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from pathlib import Path

CLEANED=Path(__file__).resolve().parents[1]/"outputs"/"pcos_cleaned.csv"

#DB connection details-> in env

load_dotenv()
#reading db details
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
#build connection string for sqlAlchemy
CONN_STR= f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_to_postgres():
   
    df = pd.read_csv(CLEANED)
    print("Loaded cleaned data with shape : ",df.shape)

    #create engine
    engine = create_engine(CONN_STR)

    #load into postgres table(replace if exists,otherwise create)
    df.to_sql("patients",engine,if_exists="replace",index=False)

    with engine.connect() as conn:
        conn.execute(text("""
        ALTER TABLE patients
        ADD COLUMN id SERIAL PRIMARY KEY;
        
        """))
        conn.commit()


    print(f"Loaded {len(df)} rows into 'patients' table in db")

#to run file independently
if __name__=="__main__":
    load_to_postgres()
    

