import time
import json
import subprocess

# Function to send the message
def send_message(dateCode):
    url = "https://jellyfinn.mooo.com/prod/send-to-user/joelv1202"
    message_data = {
        "message": f"Tickets for {dateCode} are here"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Send the JSON message
    response = requests.post(url, json=message_data, headers=headers)
    
    if response.status_code == 204:
        print(f"Message sent for {dateCode}.")
    else:
        print(f"Failed to send message for {dateCode}.")

def get_nested_value(data, path):
    """
    Retrieves a value from a nested data structure by following a path of keys/indices.
    
    Args:
        data: The nested data structure (dict, list, etc.) to traverse
        path: A list of keys or indices to navigate through the nested structure
        
    Returns:
        The value at the specified path or None if the path is invalid
        
    Example:
        data = {"fruits": [{"label": {"carbohydrates": {"nutrition": 25}}}]}
        get_nested_value(data, ["fruits", 0, "label", "carbohydrates", "nutrition"])
        # Returns 25
    """
    current = data
    
    try:
        for key in path:
            current = current[key]
        return current
    except (KeyError, IndexError, TypeError):
        return None

def check_showtimes(dateCode):
    curl_command = r"""curl 'https://api3.pvrcinemas.com/api/v1/booking/content/msessions'   -H 'accept: application/json, text/plain, */*'   -H 'accept-language: en-US,en;q=0.7'   -H 'appversion: 1.0'   -H 'authorization: Bearer'   -H 'cache-control: no-cache'   -H 'chain: PVR'   -H 'city: Navi Mumbai'   -H 'content-type: application/json'   -H 'country: INDIA'   -H 'origin: https://www.pvrcinemas.com'   -H 'platform: WEBSITE'   -H 'pragma: no-cache'   -H 'priority: u=1, i'   -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"'   -H 'sec-ch-ua-mobile: ?0'   -H 'sec-ch-ua-platform: "Windows"'   -H 'sec-fetch-dest: empty'   -H 'sec-fetch-mode: cors'   -H 'sec-fetch-site: same-site'   -H 'sec-gpc: 1'   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'   --data-raw '{"city":"Navi Mumbai","mid":"31737","experience":"ALL","specialTag":"ALL","lat":"19.134393","lng":"72.831393","lang":"ALL","format":"ALL","dated":"2025-07-27","time":"08:00-24:00","cinetype":"ALL","hc":"ALL","adFree":false}'"""

    # Execute the curl command using subprocess
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True, encoding='utf-8', shell=True)
        print("Curl command executed successfully.", result.stdout)
        data = json.loads(result.stdout)

        date = get_nested_value(data, ['output', 'movieCinemaSessions', 0, 'experienceSessions', 0, 'shows', 0, 'showDateStr'])
        if date == dateCode:
            print(f"DateCode {dateCode} matches! Sending message...")
            send_message(dateCode)
        else:
            print(f"DateCode {dateCode} does not match.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute curl command. Error: {e}")
    except UnicodeDecodeError as e:
        print(f"Unicode decode error: {e}")

# Main loop that calls the API every 30 seconds
def main():
    # Set your dateCode here
    dateCode = "2025-07-27"  # You can modify this dynamically as per requirement
    
    while True:
        print(f"Checking showtimes for {dateCode}...")
        check_showtimes(dateCode)
        
        # Wait for 30 seconds before calling again
        time.sleep(30)

if __name__ == "__main__":
    main()
