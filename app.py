from flask import Flask, render_template,request
from dotenv import load_dotenv
from datetime import datetime
import requests,os

app = Flask(__name__)

load_dotenv()
API_KEY=os.getenv("APP_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "feels_like":data["main"]["feels_like"],
                "temp_min":data["main"]["temp_min"],
                "temp_max":data["main"]["temp_max"],
                "description": data["weather"][0]["description"].capitalize(),
                "icon": data["weather"][0]["icon"],
                "humidity":data["main"]["humidity"],
                "pressure":data["main"]["pressure"],
                "wind":data["wind"]["speed"],
                "gust":data["wind"]["gust"],
            }
        else:
            weather_data = {"error": "City not found"}
        print(data)
    return render_template("index.html", weather=weather_data)


if __name__=='__main__':
    app.run(debug=True,port=8000)