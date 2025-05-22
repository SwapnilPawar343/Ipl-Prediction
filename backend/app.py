from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model and columns
try:
    model = joblib.load('model.pkl')
    columns = joblib.load('columns.pkl')
    print("Model and columns loaded successfully.")
except Exception as e:
    print(f"Error loading model or columns: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("Received Data:", data)  # Debugging
        
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Convert incoming JSON to DataFrame
        input_data = pd.DataFrame([data])
        
        # Load the saved encoder and features list
        encoder = joblib.load('encoder.pkl')
        saved_features = joblib.load('features.pkl')

        # Transform the input data using the saved encoder
        input_encoded = encoder.transform(input_data)
        
        # Align the columns of the input data to match training data
        input_encoded_df = pd.DataFrame(input_encoded, columns=encoder.get_feature_names_out(saved_features))

        # Reorder columns to match model training
        all_columns = encoder.get_feature_names_out(saved_features)
        input_encoded_df = input_encoded_df.reindex(columns=all_columns, fill_value=0)

        # Load the model
        model = joblib.load('model.pkl')

        # Make prediction
        prediction = model.predict(input_encoded_df)
        result = {'prediction': prediction[0]}
        return jsonify(result)

    except Exception as e:
        print("❌ Error during prediction:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
