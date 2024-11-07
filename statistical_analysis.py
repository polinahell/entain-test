import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import psycopg2

DATABASE = "entain_test"
USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = "5434"

connection = psycopg2.connect(
    dbname=DATABASE,
    user=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

query = """
    SELECT user_id,
           COUNT(*) FILTER (WHERE type = 'bet') AS total_bets,
           SUM(amount) FILTER (WHERE type = 'bet') AS total_amount_bet,
           COUNT(*) FILTER (WHERE type = 'win') AS total_wins,
           SUM(amount) FILTER (WHERE type = 'win') AS total_amount_won,
           SUM(CASE WHEN type = 'win' THEN amount ELSE -amount END) AS net_profit,
           AVG(amount) FILTER (WHERE type = 'bet') AS avg_bet_amount
    FROM parsed_data
    GROUP BY user_id;
"""

user_features = pd.read_sql_query(query, con=connection)

connection.close()

user_features.fillna(0, inplace=True)

print(user_features.head())

X = user_features[['total_bets', 'total_amount_bet', 'total_wins', 'total_amount_won', 'avg_bet_amount']]
y = user_features['net_profit']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

r_squared = model.score(X_test, y_test)
print(f"R-squared on test data: {r_squared:.2f}")

predictions = model.predict(X)

user_features['predicted_net_profit'] = predictions

most_profitable_user = user_features.loc[user_features['predicted_net_profit'].idxmax(), 'user_id']
print(f"User with the highest predicted profit in December: {most_profitable_user}")

output_file = r"C:\Users\37259\Desktop\Programming\entain-test\data\analysis.csv"
user_features.to_csv(output_file, index=False)

print(f"Predictions saved to {output_file}")
