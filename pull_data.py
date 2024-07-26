import requests
import json
import time
import os

# Function to log in and get session ID
def login(api_url, username, password):
    login_url = f"{api_url}/session"
    payload = {
        "user": username,
        "password": password
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    response = requests.post(login_url, headers=headers, json=payload, verify=False)
    response.raise_for_status()
    session_id = response.cookies.get('session_id')
    return session_id

# Function to log out
def logout(api_url, session_id):
    logout_url = f"{api_url}/session"
    headers = {
        "accept": "application/json",
        "Cookie": f"session_id={session_id}"
    }
    
    response = requests.delete(logout_url, headers=headers, verify=False)
    response.raise_for_status()

# Function to grab data
def grab_data(api_url, session_id, interval, duration, output_file):
    kpi_url = f"{api_url}/kpi"
    payload = {
        "ids": ["MEM_STATS"]
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Cookie": f"session_id={session_id}"
    }
    
    end_time = time.time() + duration
    all_data = []
    
    while time.time() < end_time:
        response = requests.post(kpi_url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        data = response.json()
        kpi_data = data.get('kpi', [])
        memory_stats = kpi_data[0].get('value', {})
        
        all_data.append(memory_stats)
        
        with open(output_file, 'w') as json_file:
            json.dump(all_data, json_file, indent=4)
        
        time.sleep(interval)

if __name__ == "__main__":
    # Get parameters from environment variables
    API_URL = os.getenv("API_URL", "https://10.80.0.100/rest")
    USERNAME = os.getenv("API_USERNAME", "admin")
    PASSWORD = os.getenv("API_PASSWORD", "admin")
    INTERVAL = int(os.getenv("API_INTERVAL", 5))
    DURATION = int(os.getenv("API_DURATION", 60))  # 1 minute
    OUTPUT_FILE = os.getenv("API_OUTPUT_FILE", "api_data.json")
    
    # Suppress SSL warnings for self-signed certificates
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    
    try:
        session_id = login(API_URL, USERNAME, PASSWORD)
        grab_data(API_URL, session_id, INTERVAL, DURATION, OUTPUT_FILE)
    finally:
        logout(API_URL, session_id)