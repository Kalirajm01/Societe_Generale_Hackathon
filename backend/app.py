from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/asset_management'
mongo = PyMongo(app)

# Asset model
model = joblib.load('predictive_model.pkl')


class Asset:
    def __init__(self, asset_type, location, status, purchase_date, maintenance_history):
        self.asset_type = asset_type
        self.location = location
        self.status = status
        self.purchase_date = purchase_date
        self.maintenance_history = maintenance_history

    def serialize(self):
        return {
            'asset_type': self.asset_type,
            'location': self.location,
            'status': self.status,
            'purchase_date': self.purchase_date,
            'maintenance_history': self.maintenance_history
        }

# Endpoint to fetch all assets


@app.route('/api/assets', methods=['GET'])
def get_assets():
    assets = list(mongo.db.assets.find())
    serialized_assets = [asset for asset in assets]
    return jsonify(serialized_assets)

# Endpoint to predict asset status


@app.route('/api/predict', methods=['POST'])
def predict_asset_status():
    data = request.get_json()  # Assuming you're sending JSON data with asset details
    # Perform any necessary data preprocessing
    # Example: Convert JSON data to pandas DataFrame
    df = pd.DataFrame(data)
    # Example: Use the loaded model to make predictions
    predictions = model.predict(df)
    # Example: Return predictions as JSON response
    return jsonify(predictions.tolist())


if __name__ == '__main__':
    app.run(debug=True)
