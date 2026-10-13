import pickle
import pandas as pd

model_is_loaded=False
with open('model/model.pkl','rb') as file:
    model=pickle.load(file)
    model_is_loaded=True

MODEL_VERSION='1.0.0'


class_labels=model.classes_.tolist()
def predict_output(user_input:dict) ->str:

    input_df=pd.DataFrame([user_input])
    prediction=model.predict(input_df)[0]
    probabilities=model.predict_proba(input_df)[0]
    confidence=max(probabilities)

    class_probs=dict(zip(class_labels, map(lambda x: round(x,4) , probabilities )))
    return {
        'predicted_category':prediction,
        'confidence':confidence,
        'class_probabilities':class_probs
    }