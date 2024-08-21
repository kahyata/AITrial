import sqlite3
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import csv


class BusinessAIModel:
    def __init__(self, db_path, csv_dir):
        self.db_path = db_path
        self.csv_dir = csv_dir
        self.model = None
        self.scaler = None
        self.label_encoders = {}

    def connect_to_db(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close_db_connection(self):
        self.conn.close()

    def fetch_data(self, query):
        return pd.read_sql_query(query, self.conn)

    def preprocess_data(self, df, categorical_features, target_feature):
        # Encode categorical features
        for feature in categorical_features:
            le = LabelEncoder()
            df[feature] = le.fit_transform(df[feature])
            self.label_encoders[feature] = le

        # Split data into features and target
        X = df.drop(columns=[target_feature])
        y = df[target_feature]

        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        return X_scaled, y

    def train_model(self, X, y):
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Train the model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Model Mean Squared Error: {mse}")

    def save_model(self, model_path):
        # Save the trained model and scaler
        joblib.dump({'model': self.model, 'scaler': self.scaler, 'label_encoders': self.label_encoders}, model_path)

    def load_model(self, model_path):
        # Load the trained model and scaler
        data = joblib.load(model_path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.label_encoders = data['label_encoders']

    def predict(self, input_data):
        # Preprocess input data
        for feature, le in self.label_encoders.items():
            input_data[feature] = le.transform([input_data[feature]])[0]

        input_df = pd.DataFrame([input_data])
        input_scaled = self.scaler.transform(input_df)

        # Predict using the trained model
        prediction = self.model.predict(input_scaled)
        return prediction[0]

    def export_to_csv(self, table_name, filename):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        file_path = os.path.join(self.csv_dir, filename)
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)
            writer.writerows(rows)

    def export_all_tables_to_csv(self, tables_to_export):
        for table, filename in tables_to_export.items():
            self.export_to_csv(table, filename)

# Set up paths
db_path = r'C:\Users\User\Desktop\Database projects\sqlite\sqlite-tools-win-x64-3460000\Sacco\src\sacco.db'
csv_dir = r'C:\Users\User\Desktop\Database projects\sqlite\sqlite-tools-win-x64-3460000\Sacco\src\csvs'

# Initialize and connect to the database
ai_model = BusinessAIModel(db_path, csv_dir)
ai_model.connect_to_db()

# Fetch and preprocess data
transactions_query = "SELECT BusinessID, Type, Category, Amount FROM Transactions"
transactions_df = ai_model.fetch_data(transactions_query)
X, y = ai_model.preprocess_data(transactions_df, categorical_features=['Type', 'Category'], target_feature='Amount')

# Train the model
ai_model.train_model(X, y)

# Save the model
model_path = os.path.join(csv_dir, 'transaction_model.pkl')
ai_model.save_model(model_path)

# Export all tables to CSV
tables_to_export = {
    'Businesses': 'Businesses.csv',
    'Transactions': 'Transactions.csv',
    'Accounts': 'Accounts.csv',
    'Invoices': 'Invoices.csv',
    'Expenses': 'Expenses.csv',
    'Revenue': 'Revenue.csv',
    'Assets': 'Assets.csv',
    'Liabilities': 'Liabilities.csv',
    'FinancialSummary': 'FinancialSummary.csv',
    'Receipts': 'Receipts.csv'
}
ai_model.export_all_tables_to_csv(tables_to_export)

# Close the database connection
ai_model.close_db_connection()

print("CSV files and model have been exported to:", csv_dir)

# Example usage of the prediction function:
ai_model.load_model(model_path)
new_data = {
    'BusinessID': 1,
    'Type': 'Income',  # This should be one of the encoded types
    'Category': 'Sales'  # This should be one of the encoded categories
}
prediction = ai_model.predict(new_data)
print(f"Predicted Amount: {prediction}")
