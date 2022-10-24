# Import important libraries
import bentoml
from pydantic import BaseModel
from bentoml.io import JSON

# Create a data schema for validation
class UserProfile(BaseModel):
    seniority: int
    home: str
    time: int
    age: int
    marital: str
    records: str
    job: str
    expenses: int
    income: float
    assets: float
    debt: float
    amount: int
    price: int

# Load the model and dictvectorizer into bentoml
model_ref = bentoml.xgboost.get("credit_risk_model:4s4pvtcth6jrgaav")
dv = model_ref.custom_objects['dictVectorizer']

# Save the model into model_runner
model_runner = model_ref.to_runner()

# Put the model into service of the bentoml API
svc = bentoml.Service("credit_risk_classifier", runners=[model_runner])

# Create the classify API function
@svc.api(input=JSON(pydantic_model=UserProfile), output=JSON())
def classify(application_data):

    # Transform the data from the pydantic class into a dictionary
    application_data = application_data.dict()
    vector = dv.transform(application_data)
    prediction = model_runner.predict.run(vector)
    print(prediction)

    # Capture the probability of being denied
    result = prediction[0]

    # Output the result based on the probabilites
    if result > 0.5:
        return {"status": "DECLINED"}
    elif result > 0.25:
        return {"status": "MAYBE"}
    else:
        return {"status":"APPROVED"}