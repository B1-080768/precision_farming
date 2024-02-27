from flask import Flask, request, render_template
import pickle
import warnings
warnings.filterwarnings("ignore")

with open('Our_Reccommendation.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return render_template('index.html')


@app.route("/classify", methods=["POST"])
def classify():

    print(request.form)
    N = int(request.form.get("N"))
    P = int(request.form.get("P"))
    K = int(request.form.get("K"))
    temperature = float(request.form.get("temperature"))
    humidity = float(request.form.get("humidity"))
    ph = float(request.form.get("ph"))
    rainfall = float(request.form.get("rainfall"))

    output = model.predict([[N, P, K, temperature, humidity, ph, rainfall]])

    d = {'rice': 1, 'maize': 2, 'chickpea': 3, 'kidneybeans': 4, 'pigeonpeas': 5,
         'mothbeans': 6, 'mungbean': 7, 'blackgram': 8, 'lentil': 9, 'pomegranate': 10,
         'banana': 11, 'mango': 12, 'grapes': 13, 'watermelon': 14, 'muskmelon': 15, 'apple': 16,
         'orange': 17, 'papaya': 18, 'coconut': 19, 'cotton': 20, 'jute': 21, 'coffee': 22}

    for i in d.values():
        if output == i:
            keys = [k for k, i in d.items() if i == output]
    result = keys[0].upper()
    return render_template('index.html', result=result,N=N, P=P, K=K, temperature=temperature, humidity=humidity, ph=ph,rainfall =rainfall)


app.run(host="0.0.0.0", port=8001, debug=True)
