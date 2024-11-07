Entain Test Task 

Overview

This project involves parsing a semi-structured dataset from a log file, storing the data in a PostgreSQL database, and performing aggregation queries along with statistical analysis to predict which user might generate the highest profit in December.


Project Structure

data/: Contains analysis.csv: Output file that contains user features and predicted net profit for December.

data_parse.py: Python script used to parse the log data and load it into the PostgreSQL database.

statistical_analysis.py: Python script for performing feature engineering and statistical analysis using scikit-learn.


Requirements

Python 3.7+

PostgreSQL

Required Python libraries:

pandas

numpy

scikit-learn

psycopg2

SQLAlchemy

Install the required libraries using:

pip install pandas numpy scikit-learn psycopg2 SQLAlchemy



Setup Instructions


Run Data Parsing Script:
Execute the script to parse data.log and load it into the database:

python data_parse.py

Run Statistical Analysis Script:


Execute the script to perform feature engineering and prediction:
python statistical_analysis.py


Statistical Analysis

The statistical_analysis.py script performs the following steps:

Feature Engineering: Calculates features such as total bets, total wins, average bet amount, and net profit for each user.

Model Training: Uses a linear regression model to predict the net profit for each user in December.

Prediction: Outputs the user with the highest predicted profit in December.

The model is trained using the historical features up to November.

Notes

Aggregation operations are performed in SQL to improve performance and reduce memory usage.
The parsing and aggregation scripts can handle large datasets, but performance may vary based on system resources.

Future Improvements

Consider using more advanced models like RandomForestRegressor.
Use cross-validation and GridSearchCV to improve model performance.
Use parallel processing to speed up data processing.

