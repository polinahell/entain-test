import re
import pandas as pd
from sqlalchemy import create_engine


data_file_path = r"C:\Users\37259\Desktop\Programming\entain-test\data\data.log"

with open(data_file_path, 'r') as file:
    data_log = file.read()

pattern = r'\[(.*?)\] \[(.*?)\] user=(\d+).*?amount=(\d+\.\d+) type=(bet|win)'

matches = re.findall(pattern, data_log)

columns = ['timestamp', 'ip_address', 'user_id', 'amount', 'type']
data = pd.DataFrame(matches, columns=columns)

data['timestamp'] = pd.to_datetime(data['timestamp'])
data['user_id'] = data['user_id'].astype(int)
data['amount'] = data['amount'].astype(float)

print(data)

DATABASE = "postgresql"
USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = "5434"
DB_NAME = "entain_test"

engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')

import psycopg2

connection = psycopg2.connect(
    dbname=DB_NAME,
    user=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

cursor = connection.cursor()
cursor.execute("TRUNCATE TABLE parsed_data;")
connection.commit()

cursor.close()
connection.close()

csv_file_path = r"C:\Users\37259\Desktop\Programming\entain-test\data\parsed_data.csv"
data.to_csv(csv_file_path, index=False, header=False)

connection = psycopg2.connect(
    dbname=DB_NAME,
    user=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

cursor = connection.cursor()
with open(csv_file_path, 'r') as f:
    cursor.copy_expert("COPY parsed_data (timestamp, ip_address, user_id, amount, type) FROM stdin WITH (FORMAT csv)", f)

connection.commit()
cursor.close()
connection.close()
