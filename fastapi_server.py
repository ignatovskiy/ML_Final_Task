from fastapi import FastAPI
import spacy


MODEL_FILENAME = "output6/model-best"


app = FastAPI()
nlp = spacy.load(MODEL_FILENAME)


@app.get("/predict")
async def predict(input_text: str):
    doc = nlp(input_text)
    cats_dict = doc.cats
    return cats_dict