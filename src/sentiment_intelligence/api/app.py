from fastapi import FastAPI
from pydantic import BaseModel
from sentiment_intelligence.predict import predict

app = FastAPI(title="Sentiment Intelligence API")

class PredictRequest(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict_endpoint(req: PredictRequest):
    return predict(req.text)
