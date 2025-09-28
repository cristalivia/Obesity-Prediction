from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn

app = FastAPI(title="Obesity Prediction API")

with open("model_XGB.pkl", "rb") as f: 
    model = joblib.load(f)

class ObesityData(BaseModel):
    Gender: str
    Age: int
    Height: float
    Weight: float
    family_history_with_overweight: str
    FAVC: str
    FCVC: float
    NCP: float
    CAEC: str
    SMOKE: str
    CH2O: float
    SCC: str
    FAF: float
    TUE: float
    CALC: str
    MTRANS: str

@app.get("/")
def read_root():
    return {"Welcome to the Obesity Prediction API"}

@app.post("/predict")
def predict(data: ObesityData):
    df = pd.DataFrame([data.dict()])

    feature_order = [
        "Gender", "Age", "Height", "Weight",
        "family_history_with_overweight", "FAVC", "FCVC", "NCP",
        "CAEC", "SMOKE", "CH2O", "SCC",
        "FAF", "TUE", "CALC", "MTRANS"
    ]
    df = df[feature_order]
    
    prediction = model.predict(df)
    print("Prediction result:", prediction)
    return {"prediction": int(prediction[0])}
