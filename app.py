from flask import Flask, jsonify  
from data_fetcher import fetch_data  
from risk_assessor import aggregate_findings  

app = Flask(__name__)  # Initialize the Flask application

# Configuration parameters: Replace these with your actual bucket and object key
BUCKET_NAME = 'enterprise-cspm'
OBJECT_KEY = 'sample_data.json'

@app.route('/api/scan', methods=['GET'])
def scan():
    """
    API Endpoint: /api/scan
    Trigger a scan to fetch data, perform risk assessment, and return the findings.
    """
    try:
        # Fetch configuration data from S3
        data = fetch_data(BUCKET_NAME, OBJECT_KEY)
        # Perform risk assessments on the fetched data
        findings = aggregate_findings(data)
        # Return a JSON response with the risk findings
        return jsonify({"status": "success", "findings": findings}), 200
    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on localhost with debugging enabled for development
    app.run(debug=True, port=5000)
