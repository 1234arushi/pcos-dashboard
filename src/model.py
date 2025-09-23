import pandas as pd
import joblib
from pathlib import Path
# python3 -m pip install scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,classification_report

CLEANED=Path(__file__).resolve().parents[1]/"outputs"/"pcos_cleaned.csv"

def train_model():
    df=pd.read_csv(CLEANED)

    #features , X->inputs and Y->answers(target labels)
    # X = df.drop(columns=["PCOS","bmi_category"])#dropping the target and leaving X->with other columns(inputs)
    selected_features=[
        "Skin_Darkening",
        "Hair_Growth",
        "Weight_Gain",
        "Cycle_Type",
        "Fast_Food",
        "Pimples",
        "Weight",
        "BMI",
        "Hair_Loss",
        "Waist",
        "Age", 
        "Cycle_Length", 
        "Marriage_Years"#negative relation
    ]
    X = df[selected_features]
    Y = df["PCOS"]

    #train/test split
    X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size = 0.2,random_state = 42,stratify = Y)

    model = LogisticRegression(max_iter=1000,class_weight="balanced")#"balanced" as we have 177->pcos(y) vs 364->pcos(n),now it will look closely to minority class
   
    model.fit(X_train,Y_train)

    #default -> p >= 0.5,predict =1 otherwise predict 0(p->probabiltiy of a patient by adding weights to the inputs)
    # Y_pred = model.predict(X_test)

    #using custom threshold,to increase recall
    Y_prob = model.predict_proba(X_test)[:,1]#predict_proba returns [P(0),P(1)]->select rows where pcos=1 because of [:,1]
    threshold = 0.4
    Y_pred = (Y_prob >= threshold).astype(int)

    acc = accuracy_score(Y_test,Y_pred)#finding right guesses
    prec = precision_score(Y_test,Y_pred)#no of cases that actually had pcos from which the model predicted had pcos=(TP/TP+FP)
    rec = recall_score(Y_test,Y_pred)#TP/TP+FN(where there was pcos)
    f1 = f1_score(Y_test,Y_pred)# avg of precision and accuracy

    print("\n Model Performance : ")
    print(f"Accuracy : {acc:.2f}")
    print(f"Precision : {prec:.2f}")
    print(f"Recall : {rec:.2f}")
    print(f"F1 score : {f1:.2f}")

    print("\n Confusion Matrix : \n",confusion_matrix(Y_test,Y_pred))
    print("\n Classification Report : \n",classification_report(Y_test,Y_pred))

    #saving the model,so that for other datasets we just need to predict from the trained model
    MODELS_DIR = Path(__file__).resolve().parents[1]/"models"
    MODELS_DIR.mkdir(parents=True,exist_ok=True)

    joblib.dump(model,MODELS_DIR/"pcos_model.pkl")
    print("Model saved at : ",MODELS_DIR/"pcos_model.pkl")#containing trained model's knowledge(the learned weights,coefficients,parameters)

    return model

if __name__=="__main__":
    trained_model = train_model()

#training set(to teach model) and test set(to check how well it trained)
#test_size ->20% of data ,rest 80% of data for training
#random_state=42(is to make sure results remain same each run meaning it is fixing the shuffling)
#for instance,that same 2 rows always go into test every run
# why 42? Hitchhiker said 42 is answer to everything
#stratify = Y (ensures that ratio of classes in Y is preserved in both train & test set)-> % non pcos & % pcos
#model=RandomForestClassifier(class_weight="balanced")->56 % recall