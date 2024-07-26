import requests
import json
import time
import os

# Function to log in and get session ID
def login(api_ip, username, password):
    try:
        login_url = f"https://{api_ip}/rest/session"
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
    
    except requests.RequestException as e:
        print(f"Login failed: {e}")
        return None

# Function to log out
def logout(api_ip, session_id):
    try:
        logout_url = f"https://{api_ip}/rest/session"
        headers = {
            "accept": "application/json",
            "Cookie": f"session_id={session_id}"
        }
        
        response = requests.delete(logout_url, headers=headers, verify=False)
        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Logout failed: {e}")

# Function to grab data
def grab_data(api_ip, session_id, interval, duration):
    try:
        kpi_url = f"https://{api_ip}/rest/kpi"
        payload = {
            "ids": ["SYSTEM_NAME", "MEM_STATS"]
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
            all_data.append({kpi_data[0].get('value'):kpi_data[1].get('value', {})})
            
            with open('api_data.json', 'w') as json_file:
                json.dump(all_data, json_file, indent=4)
            
            time.sleep(interval)

    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")

if __name__ == "__main__":
    # Get parameters from environment variables
    API_IP = os.getenv("API_IP", "10.80.0.100")
    USERNAME = os.getenv("API_USERNAME", "admin")
    PASSWORD = os.getenv("API_PASSWORD", "admin")
    INTERVAL = int(os.getenv("API_INTERVAL", 5))
    DURATION = int(os.getenv("API_DURATION", 30))
    
    # Suppress SSL warnings for self-signed certificates
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    
    try:
        session_id = login(API_IP, USERNAME, PASSWORD)
        grab_data(API_IP, session_id, INTERVAL, DURATION)
    finally:
        logout(API_IP, session_id)
