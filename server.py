from flask import Flask, request, render_template
import pickle
import warnings
warnings.filterwarnings("ignore")

# load the model
# with open('../../models/cb.pkl', 'rb') as file:
#with open('/home/user/Downloads/Precision_farming_final/Fertilizer.pkl', 'rb') as file:/
# with open('/home/user/Documents/Project_PF/Fertilizer_UI/Fertilizer.pkl', 'rb') as file:
#     model = pickle.load(file)

with open("Fertilizer.pkl" , "rb") as file:
    model = pickle.load(file)

# create a flask application
app = Flask(__name__)


@app.route("/", methods=['GET'])
def root():
    # read the file contents and send them to client
    # return render_template('index.html')

    return render_template('index.html')


@app.route("/classify", methods=["POST"])
def classify():
    # get the values entered by user66
    print(request.form)
    Temperature = float(request.form.get("Temperature"))
    Humidity = float(request.form.get("Humidity"))
    Rainfall = float(request.form.get("Rainfall"))
    pH = float(request.form.get("pH"))
    N = float(request.form.get("N"))
    P = float(request.form.get("P"))
    K= float(request.form.get("K"))
    Soil = str(request.form.get("Soil"))
    Crop = str(request.form.get("Crop"))

    print(Temperature)

    Soil_dict = {'Clayey': 1, 'laterite': 2, 'silty clay': 3, 'sandy': 4, 'coastal': 5, 'clay loam': 6, 'alluvial': 7}

    Crop_dict = {'rice': 1, 'Coconut': 2}

    print(Soil_dict.get(Soil), Crop_dict.get(Crop))

    output = model.predict([
        [Temperature, Humidity, Rainfall, pH, N, P, K, Soil_dict.get(Soil), Crop_dict.get(Crop) ]
                            ])

    d = {'DAP and MOP': 1, 'Good NPK' : 2, 'MOP' : 3, 'Urea and DAP': 4, 'Urea and MOP': 5,'Urea': 6, 'DAP': 7}

    ans = " "

    for i in d.values():
        if output == i:
            keys = [k for k, i in d.items() if i == output]
            ans += keys[0]
    # return ("Recommended fertilizer : ", ans)
    result = ans
    print(result)
    return render_template('index.html',result=result,
                           Temperature=Temperature,
                           Humidity = Humidity,
                           Rainfall = Rainfall,
                           pH=pH,
                           N=N,
                           P=P,
                           K=K,
                           Soil=Soil_dict.get(Soil),
                           Crop=Crop_dict.get(Crop))


# start the application
app.run(host="0.0.0.0", port=8002, debug=True)

