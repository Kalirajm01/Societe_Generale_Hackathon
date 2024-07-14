import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from app import mongo
from flask_pymongo import PyMongo

# Load dataset
df = pd.read_csv('assets_dataset.csv')

# Feature engineering (example: using maintenance history count as a feature)
df['maintenance_count'] = df['MaintenanceHistory'].apply(
    lambda x: len(eval(x)))

# Define features and target
X = df[['maintenance_count']]  # Example feature
y = df['Status']  # Example target (status)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train a model (example using Random Forest)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy}')

# Example: Save the trained model for future use
joblib.dump(model, 'predictive_model.pkl')


# Example: Load trained model and make predictions for new data
model = joblib.load('predictive_model.pkl')

# Example: Predict using new data
new_data = pd.DataFrame({'maintenance_count': [3]})
prediction = model.predict(new_data)[0]

# Example: Store prediction in MongoDB
mongo.db.assets.insert_one({
    'asset_type': 'Server',
    'location': 'Data Center A',
    'status': prediction,
    'purchase_date': '2023-01-01',
    'maintenance_history': [{'date': '2023-02-15', 'details': 'Routine maintenance'}]
})
