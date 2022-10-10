import pickle

# Load the model and dict-vectorizer
model_file = 'model1.bin'
dv_file = 'dv.bin'


with open(model_file, 'rb') as model_in, open(dv_file, 'rb') as dv_in:
    model = pickle.load(model_in)
    dv = pickle.load(dv_in)

# Score one client
client = {
    "reports": 0, 
    "share": 0.001694, 
    "expenditure": 0.12, 
    "owner": "yes"
}

def predict(model, dv, client):
    X = dv.transform([client])
    pred = model.predict_proba(X)[0, 1]

    return pred

print(predict(model, dv, client))