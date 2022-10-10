import pickle
from flask import Flask
from flask import request
from flask import jsonify

# Load the model with pickle
model_file = 'model1.bin'
dv_file = 'dv.bin'

with open(model_file, 'rb') as model_in, open(dv_file, 'rb') as dv_in:
    model = pickle.load(model_in)
    dv = pickle.load(dv_in)

# Flask application name
app = Flask('credit')

@app.route('/predict', methods=['POST'])
def predict():

    # Obtain prediction
    client = request.get_json()
    X = dv.transform([client])
    y_pred = model.predict_proba(X)[0,1]
    credit = y_pred >= 0.5

    # Output a dictionary for an answer
    result = {
        "credict_probability": float(y_pred),
        "credit_card": bool(credit)
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)