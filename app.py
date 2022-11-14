#Flask,scikit-learn,pandas,pickle-mixin
from flask import Flask,render_template,request
import pandas as pd
import numpy as np
import pickle
 
app=Flask(__name__)
data=pd.read_csv('Cleaned_data.csv')

@app.route('/')
def index():
    locations =sorted(data['location'].unique())
    
    return render_template('index.html',locations=locations)

__locations = None
__data_columns = None
model = pickle.load(open("bangalore_home_prices_model.pickle","rb"))


def get_estimated_price(input_json):
    try:
        loc_index = __data_columns.index(input_json['location'].lower())
    except:
        loc_index = -1
    x = np.zeros(244)
    x[0] = input_json['sqft']
    x[1] = input_json['bath']
    x[2] = input_json['bhk']
    if loc_index >= 0:
        x[loc_index] = 1
    result = round(model.predict([x])[0],2)
    if(x[0]==0 or x[2]==0):
        result=0
    elif(result<=0):
        result=0
    return result


@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        input_json = {
            "location": request.form['location'],
            "sqft": request.form['total_sqft'],
            "bhk": request.form['bhk'],
            "bath": request.form['bath']
        }
        result = get_estimated_price(input_json)
        print(result)
        if result==0:
            result="you cannot predict with given values"
            return render_template('predict.html',result=result)
        elif result > 100:
            result = round(result/100, 2)
            result = str(result) + ' Crore'
        else:
            result = str(result) + ' Lakhs'
        return render_template('predict.html',result=result)

if __name__ == "__main__":
    app.run(debug=True,port=5001)