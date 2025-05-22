import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
import joblib
import numpy as np

# Load your dataset (replace with your dataset path)
data = pd.read_csv('data1.csv')

# Drop rows with missing values
data.dropna(inplace=True)

# Define your target variable and features
target = 'winner'
features = ['season', 'city', 'team1', 'team2', 'toss_winner', 'toss_decision', 'venue']

X = data[features]
y = data[target]

# One-Hot Encoding for categorical variables
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_encoded = encoder.fit_transform(X)

# Save encoder for prediction usage
joblib.dump(encoder, 'encoder.pkl')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Evaluate the model
print("Training Accuracy:", accuracy_score(y_train, y_pred_train))
print("Testing Accuracy:", accuracy_score(y_test, y_pred_test))
print("Classification Report:\n", classification_report(y_test, y_pred_test))

# Save the model and column names
joblib.dump(model, 'model.pkl')
joblib.dump(features, 'features.pkl')

print(" Model and encoder saved successfully!")
