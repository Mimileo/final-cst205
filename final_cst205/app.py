from flask import Flask, render_template, request
import requests, json

app = Flask(__name__)

@app.route('/temperature', methods=['POST'])
def temperature():
    zipcode = request.form['zip']
    url = 'http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid=59903fb79cf3bf6d95a4d822609b0402&q='
    
    json_object = requests.get(url).json()
    item = requests.get(url).json()
    temp_k = item['main']['temp']
    temp_f = (temp_k - 273.15) * 1.8 + 32
    temp = round(temp_f,2)
    return temp
    #temperature = json_object['main']['temp']
    #temp_k = float(json_object['main']['temp'])
    #return temperature

   
    '''json_object = r.json()
    temp_k = float(json_object['main']['temp'])
    temp_f = (temp_k - 273.15) * 1.8 + 32
    return render_template('temperature.html', temp=temp_f)'''

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)