from flask import Flask, request, jsonify
import joblib
import pandas as pd
import tldextract
import re
import whois
import requests
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model
MODEL_PATH = "phishing_rf_model.pkl"
model = joblib.load(MODEL_PATH)

# Define feature columns
FEATURE_COLUMNS = ['Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
                   'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic',
                   'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards']

def get_domain_info(url):
    """Fetch WHOIS domain information"""
    try:
        domain = tldextract.extract(url).registered_domain
        whois_info = whois.whois(domain)
        
        # Calculate domain age (years)
        creation_date = whois_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        domain_age = (time.time() - creation_date.timestamp()) / (365 * 24 * 3600) if creation_date else 0
        
        # Check DNS record availability
        dns_record = 1 if whois_info.domain_name else 0
        
        return domain_age, dns_record
    except:
        return 0, 0  # Default values if WHOIS lookup fails

def get_web_traffic(url):
    """Estimate web traffic (Simplified)"""
    try:
        response = requests.get(url, timeout=3)
        return 10 if response.status_code == 200 else 1
    except:
        return 0  # Assume no traffic if site is unreachable

def extract_features(url):
    """Extract features from the given URL."""
    domain_age, dns_record = get_domain_info(url)
    web_traffic = get_web_traffic(url)
    
    features = {
        "Have_IP": 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,
        "Have_At": 1 if "@" in url else 0,
        "URL_Length": len(url),
        "URL_Depth": url.count("/"),
        "Redirection": 1 if "//" in url[7:] else 0,
        "https_Domain": 1 if "https" in url[:8] else 0,
        "TinyURL": 1 if len(url) < 20 and "." not in url[7:] else 0,
        "Prefix/Suffix": 1 if "-" in tldextract.extract(url).domain else 0,
        "DNS_Record": dns_record,
        "Web_Traffic": web_traffic,
        "Domain_Age": domain_age,
        "Domain_End": 1 if ".com" in url or ".org" in url else 0,
        "iFrame": 0,  # Placeholder, real implementation needed
        "Mouse_Over": 0,  # Placeholder, real implementation needed
        "Right_Click": 1,  # Placeholder, real implementation needed
        "Web_Forwards": 0  # Placeholder, real implementation needed
    }
    return features

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        url = data.get("url")
        
        if not url:
            return jsonify({"error": "No URL provided"}), 400
        
        # Extract features from URL
        features = extract_features(url)
        df = pd.DataFrame([features])
        
        # Make prediction
        prediction = model.predict(df)[0]
        result = "phishing" if prediction == 1 else "legitimate"
        
        return jsonify({"url": url, "prediction": result})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
