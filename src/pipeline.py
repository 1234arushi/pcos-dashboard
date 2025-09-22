from src.transform import transform
from src.load import load_to_postgres

def run_pipeline():
    print("Starting ETL pipeline")
    try:
        df_clean = transform()
        print(f"Transformed data with shape {df_clean.shape}")
    except Exception as e:
        print("Error running transform script:",str(e))
        sys.exit(1)#stop pipeline immediately


    try:
        load_to_postgres()
        print("Loaded data into PostgreSQL")

    except Exception as e:
        print("Error running load script:",str(e))
        sys.exit(1)#stop pipeline immediately

    print("ETL pipeline finished successfully!")

if __name__=="__main__":
    run_pipeline()

# python3 -m src.pipeline   