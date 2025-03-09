import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
file_path = "backend/phishing_url.csv"  # Update path if needed
df = pd.read_csv(file_path)

print("Columns in dataset:", df.columns)

# Strip spaces from column names
df.columns = df.columns.str.strip()

# Print sample target values
print(df["Label"].head())

# Encode the target variable
label_encoder = LabelEncoder()
df["Label"] = label_encoder.fit_transform(df["Label"])  # phishing = 1, legitimate = 0

# Drop the 'Domain' column if it's not needed (since 'url' doesn't exist)
df.drop(columns=["Domain"], inplace=True)  # Change this if needed

# Split the dataset
X = df.drop(columns=["Label"])
y = df["Label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train the Random Forest classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions
y_pred = rf_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Model Accuracy: {accuracy:.4f}\n")
print("Classification Report:\n", report)

# Save the trained model
joblib.dump(rf_model, "backend/phishing_rf_model.pkl")
