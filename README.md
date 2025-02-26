# Cloud Security Posture Management (CSPM) Tool

So last night, one of my mentees approached me with a question: *"How can I build a project that not only teaches me cloud security but also gives me real hands-on experience with assessing cloud environments?"* They were eager to understand how to evaluate cloud resources against industry standards and secure them against misconfigurations. After discussing various ideas, I decided on creating a Cloud Security Posture Management (CSPM) tool. This project would teach them the fundamentals of AWS configuration, risk assessment, and how to build an API and dashboard for real-time security monitoring.

## Project Overview

The CSPM tool is designed to continuously assess your AWS cloud environment against security benchmarks like CIS and NIST guidelines. It simulates real-world scenarios by using sample data stored in an S3 bucket and performs risk assessments on:

- **IAM Configurations:** Checking for overly permissive roles.
- **S3 Buckets:** Identifying public access or unencrypted storage.
- **EC2 Instances:** Flagging instances with public IP addresses.
- **Security Groups:** Verifying inbound/outbound rules against security best practices.

The tool includes a Flask-based API to trigger scans and return risk findings, as well as a simple dashboard to visualize these findings.

## Table of Contents

- [Introduction: A Story of Mentorship](#introduction-a-story-of-mentorship)
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
  - [Running the API](#running-the-api)
  - [Viewing the Dashboard](#viewing-the-dashboard)
- [Screenshots](#screenshots)

## Project Structure

```
cspm-tool/
├── app.py                  # Main Flask application for API and dashboard
├── data_fetcher.py         # Module for fetching configuration data from S3
├── risk_assessor.py        # Module for performing risk assessments on the data
└── templates/
    └── dashboard.html      # HTML template for the dashboard
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- An AWS account with S3 access (for storing sample JSON data)
- AWS CLI configured with proper credentials

### Installation Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/cspm-tool.git
   cd cspm-tool
   ```

2. **Set Up a Virtual Environment and Install Dependencies:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Upload Sample Data:**

   - Create an S3 bucket (e.g., `enterprise-cspm-sample`).
   - Upload your sample JSON file (e.g., `sample_data.json`) that contains enterprise-like AWS configurations.

## Usage

### Running the Flask API

1. **Start the Flask Application:**

   ```bash
   python app.py
   ```

2. **Access the API Endpoint:**

   - Visit `http://localhost:5000/api/scan` in your browser or use Postman/cURL. This endpoint triggers a scan, fetches configuration data from S3, performs risk assessments, and returns a JSON response with the findings.

### Viewing the Dashboard

1. **Open the Dashboard:**

   - Navigate to `http://localhost:5000/` in your browser.
   - Click the **Run Scan** button to trigger the API call and view the risk findings directly on the dashboard.

## Deep Dive: API & Dashboard Integration

### Flask API

The Flask API serves as the backbone of our CSPM tool. The key endpoint `/api/scan` works as follows:

- **Data Fetching:**  
  The API calls `fetch_sample_data` (from `data_fetcher.py`) to retrieve sample configuration data from S3.

- **Risk Assessment:**  
  The data is passed to `aggregate_findings` (in `risk_assessor.py`), which runs various checks (e.g., public access on S3, overly permissive IAM roles) and produces a list of findings.

- **Response:**  
  Findings are returned as a JSON response.

*Key Code Snippet:*

```python
@app.route('/api/scan', methods=['GET'])
def scan():
    try:
        data = fetch_sample_data(BUCKET_NAME, OBJECT_KEY)
        findings = aggregate_findings(data)
        return jsonify({"status": "success", "findings": findings}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
```

### Dashboard Integration

We provide two options for the dashboard:

1. **Using Flask's Templating Engine (Jinja2):**
   - A simple HTML file (`dashboard.html`) in the `templates` folder displays findings.
   - JavaScript within the HTML makes an asynchronous call to `/api/scan` and dynamically updates the dashboard with the scan results.

2. **Using a Modern Frontend Framework (e.g., React):**
   - For a richer UI, you could build a separate React app that consumes the API.
   - In this project, we use Jinja2 for simplicity.

*Dashboard Code Highlights (dashboard.html):*

```html
<!DOCTYPE html>
<html>
<head>
    <title>CSPM Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .finding { border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
        .Critical { background-color: #f8d7da; }
        .High { background-color: #fff3cd; }
        .Medium { background-color: #d1ecf1; }
    </style>
</head>
<body>
    <h1>Cloud Security Posture Management Dashboard</h1>
    <button onclick="runScan()">Run Scan</button>
    <div id="results"></div>

    <script>
        async function runScan() {
            const response = await fetch('/api/scan');
            const data = await response.json();
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';

            if (data.status === "success") {
                data.findings.forEach(finding => {
                    const div = document.createElement('div');
                    div.classList.add('finding', finding.severity);
                    div.innerHTML = `<strong>Resource:</strong> ${finding.resource}<br>
                                     <strong>Issue:</strong> ${finding.issue}<br>
                                     <strong>Severity:</strong> ${finding.severity}`;
                    resultsDiv.appendChild(div);
                });
            } else {
                resultsDiv.innerHTML = `<p>Error: ${data.message}</p>`;
            }
        }
    </script>
</body>
</html>
```
# Screenshots 
![Screenshot 2025-02-26 at 6 21 24 PM](https://github.com/user-attachments/assets/5cc4e78a-e405-4a62-9a07-018880aedcaa)

![Screenshot 2025-02-26 at 6 28 54 PM](https://github.com/user-attachments/assets/9a152e72-ac3f-4fc2-978e-b2270afc5ffc)
 


