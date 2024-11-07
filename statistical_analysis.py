import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import psycopg2

# Database credentials
DATABASE = "entain_test"
USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = "5434"

# Step 1: Load Pre-Aggregated Data from PostgreSQL
# Connect to the database using psycopg2
connection = psycopg2.connect(
    dbname=DATABASE,
    user=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

# Pre-aggregated SQL query
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

# Load aggregated data into a DataFrame
user_features = pd.read_sql_query(query, con=connection)

# Close the connection
connection.close()

# Fill NaN values with 0 (for users with no bets or wins)
user_features.fillna(0, inplace=True)

print("Features for each user:")
print(user_features.head())

# Step 2: Model Training
# Define features (X) and target (y)
X = user_features[['total_bets', 'total_amount_bet', 'total_wins', 'total_amount_won', 'avg_bet_amount']]
y = user_features['net_profit']

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
r_squared = model.score(X_test, y_test)
print(f"R-squared on test data: {r_squared:.2f}")

# Step 3: Prediction
# Predict net profit for each user for December
predictions = model.predict(X)

# Add predictions to the user_features DataFrame
user_features['predicted_net_profit'] = predictions

# Find the user with the highest predicted profit for December
most_profitable_user = user_features.loc[user_features['predicted_net_profit'].idxmax(), 'user_id']
print(f"User with the highest predicted profit in December: {most_profitable_user}")

# Save the prediction results if needed
output_file = r"C:\Users\37259\Desktop\Programming\Entain\entain-test\data\analysis.csv"
user_features.to_csv(output_file, index=False)

print(f"Predictions saved to {output_file}")
