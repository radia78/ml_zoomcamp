# Import important libraries
import bentoml
from bentoml.io import JSON
from bentoml.io import NumpyNdarray

# Load the model and dictvectorizer into bentoml
model_ref = bentoml.sklearn.get("mlzoomcamp_homework:jsi67fslz6txydu5")

# Save the model into model_runner
model_runner = model_ref.to_runner()

# Put the model into service of the bentoml API
svc = bentoml.Service("credit_risk_classifier", runners=[model_runner])

# Create the classify API function
@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def classify(vector):

    # Transform the data from numpy array into a dictionary
    prediction = model_runner.predict.run(vector)
    print(prediction)

    # Capture the probability of being denied
    result = prediction[0]

    return result