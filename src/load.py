import pandas as pd
from sqlalchemy import create_engine,text
from pathlib import Path

CLEANED=Path(__file__).resolve().parents[1]/"outputs"/"pcos_cleaned.csv"

#DB connection details
DB_USER = "postgres"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "pcos_db"

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

if __name__=="__main__":
    load_to_postgres()
    

