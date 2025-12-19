from flask import Flask, render_template
import requests
from datetime import date

app = Flask(__name__)

@app.route('/')
def index():
    # Bugünün tarihini al (YYYY-MM-DD formatında)
    today = str(date.today())
    
    # NASA API'sine istek at (DEMO_KEY kullanıyoruz)
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key=DEMO_KEY"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # O günkü asteroid listesini al
        asteroids = data['near_earth_objects'][today]
        
        processed_data = []
        hazardous_count = 0
        
        for ast in asteroids:
            # Tehlikeli mi?
            is_hazardous = ast['is_potentially_hazardous_asteroid']
            if is_hazardous:
                hazardous_count += 1
            
            # Verileri basitleştir
            ast_data = {
                'name': ast['name'],
                'size': round(ast['estimated_diameter']['meters']['estimated_diameter_max'], 1), # Metre cinsinden çap
                'speed': round(float(ast['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']), 0), # Hız
                'distance': round(float(ast['close_approach_data'][0]['miss_distance']['kilometers']), 0), # Mesafe
                'hazardous': is_hazardous
            }
            processed_data.append(ast_data)
            
        # En hızlı asteroidi bulup öne çıkarmak için sıralayalım
        processed_data.sort(key=lambda x: x['size'], reverse=True)

        return render_template('index.html', 
                             asteroids=processed_data, 
                             count=len(processed_data),
                             hazardous_count=hazardous_count,
                             date=today)
                             
    except Exception as e:
        return f"NASA bağlantısında hata oluştu: {e}"

if __name__ == '__main__':
    app.run(debug=True)