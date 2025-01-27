from flask import Flask, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="test@123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS public.sensor_data (
        id SERIAL PRIMARY KEY,
        temperature FLOAT,
        humidity FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

@app.route('/', methods=['POST'])  # Ensure POST method is specified here
def index():
    data = request.json
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    cursor.execute(
        """INSERT INTO public.sensor_data (temperature, humidity) VALUES (%s, %s)""",
        (temperature, humidity)
    )
    conn.commit()

    return "Data Inserted", 200

@app.route('/data', methods=['GET'])  # Add GET method to retrieve data
def get_data():
    cursor.execute("SELECT * FROM public.sensor_data")
    rows = cursor.fetchall()
    return {'data': rows}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
