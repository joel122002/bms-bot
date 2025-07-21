import requests
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

def check_showtimes(dateCode):
    curl_command = [
        'curl', f'https://in.bookmyshow.com/api/v3/mobile/showtimes/byvenue?dateCode={dateCode}&venueCode=CSWO&regionCode=MUMBAI&memberId=&bmsId=1.719737512.1753069002002&appCode=WEBV2&token=26x3aab5x746514b3b7b&lsId=',
        '-H', 'x-app-code: WEB',
        '-H', 'sec-ch-ua-platform: "Windows"',
        '-H', 'Referer: https://in.bookmyshow.com/cinemas/mumbai/cinepolis-nexus-seawoods-nerul-navi-mumbai/buytickets/CSWO/20250723',
        '-H', 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        '-H', 'sec-ch-ua-mobile: ?0',
        '-H', r'baggage: sentry-environment=production,sentry-release=release_3790,sentry-public_key=4d17a59c2597410e714ab31d421148d9,sentry-trace_id=c772da57d3e24166baf0370de27b060d,sentry-transaction=%2Fcinemas%2F%3AregionNameSlug%2F%3AvenueNameSlug%2Fbuytickets%2F%3AvenueCode%2F%3AshowDate%3F,sentry-sampled=false,sentry-sample_rand=0.09049261958270327,sentry-sample_rate=0.001',
        '-H', 'sentry-trace: c772da57d3e24166baf0370de27b060d-b597d4ce72e895a9-0',
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        '-H', 'Accept: application/json, text/plain, */*',
        '-H', 'x-region-code: MUMBAI'
    ]

    # Execute the curl command using subprocess
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True, encoding='utf-8')
        print("Curl command executed successfully.", result.stdout)
        data = json.loads(result.stdout)

        # Check if the response contains ShowDetails and compare the date
        if 'ShowDetails' in data and len(data['ShowDetails']) > 0:
            if data['ShowDetails'][0].get('Date') == dateCode:
                print(f"DateCode {dateCode} matches! Sending message...")
                send_message(dateCode)
            else:
                print(f"DateCode {dateCode} does not match.")
        else:
            print("No ShowDetails found in the response.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute curl command. Error: {e}")
    except UnicodeDecodeError as e:
        print(f"Unicode decode error: {e}")

# Main loop that calls the API every 30 seconds
def main():
    # Set your dateCode here
    dateCode = "20250723"  # You can modify this dynamically as per requirement
    
    while True:
        print(f"Checking showtimes for {dateCode}...")
        check_showtimes(dateCode)
        
        # Wait for 30 seconds before calling again
        time.sleep(30)

if __name__ == "__main__":
    main()
