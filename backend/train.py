import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


file_path = "backend/phishing_url.csv"  
df = pd.read_csv(file_path)

print("Columns in dataset:", df.columns)


df.columns = df.columns.str.strip()


print(df["Label"].head())


label_encoder = LabelEncoder()
df["Label"] = label_encoder.fit_transform(df["Label"])  


df.drop(columns=["Domain"], inplace=True)  

X = df.drop(columns=["Label"])
y = df["Label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)


y_pred = rf_model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Model Accuracy: {accuracy:.4f}\n")
print("Classification Report:\n", report)


joblib.dump(rf_model, "backend/phishing_rf_model.pkl")
