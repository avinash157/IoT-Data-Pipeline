def convert_and_insert_data():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="test@123",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Fetch latest data from sensor_data table
    cursor.execute("SELECT temperature, humidity, timestamp FROM public.sensor_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        temperature, humidity, timestamp = row
        fahrenheit = (temperature * 9/5) + 32

        # Insert data into metric table
        cursor.execute("INSERT INTO public.metric (metric_time, celsius, fahrenheit) VALUES (%s, %s, %s)", 
                       (timestamp, temperature, fahrenheit))
        conn.commit()

    conn.close()
    time.sleep(25)  # Wait for 25 seconds before the next execution

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'sensor_data_ingestion',
    default_args=default_args,
    description='A simple DAG to insert processed sensor data into Postgres',
    schedule_interval='*/1 * * * *',  # Run every minute
)

t1 = PythonOperator(
    task_id='convert_and_insert_data',
    python_callable=convert_and_insert_data,
    dag=dag,
)