import time
import json
import subprocess
from string import Template
from utils import get_nested_value, send_message, get_logger, error_handler

# Get logger for this module
logger = get_logger('blinkit_bot')

def check_showtimes(dateCode):
    curl_command_template = Template(r"""curl_chrome116 'https://blinkit.com/v1/layout/product/488035' -X 'POST' -H 'accept: */*' -H 'accept-language: en-US,en;q=0.9' -H 'access_token: null' -H 'app_client: consumer_web' -H 'app_version: 1010101010' -H 'auth_key: c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477' -H 'cache-control: no-cache' -H 'content-length: 0' -H 'content-type: application/json' -b 'gr_1_deviceId=a505e41c-7102-4453-bbae-aac4d15ee794; city=; __cfruid=8af78256499815a9c8409697599c31545aa6a770-1754021250; _cfuvid=wjFDTIeQliMcPhbH0uVjICZUWafWOMY71fvYlRGAAo0-1754021250359-0.0.1.1-604800000; gr_1_locality=Navi%20Mumbai; __cf_bm=Z7Inyf8.rFR9lZUujmjrtx94HT5onzHfQ3TkErW_UMc-1754024972-1.0.1.1-egNn8NG5LqS2eLfMKXZ4CReubV6LBOan3Tvd..bFELbcPUZ87fxJQL4jQc_l7M4AAPEF61HLS0LKhp80HlEWyZbbeoKgJe54GO2pnSDGirs; gr_1_lat=19.027063; gr_1_lon=73.0275115; gr_1_landmark=undefined' -H 'device_id: a505e41c-7102-4453-bbae-aac4d15ee794' -H 'lat: 19.027063' -H 'lon: 73.0275115' -H 'origin: https://blinkit.com' -H 'pragma: no-cache' -H 'priority: u=1, i' -H 'referer: https://blinkit.com/prn/x/prid/488035' -H 'rn_bundle_version: 1009003012' -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"' -H 'sec-ch-ua-mobile: ?0' -H 'sec-ch-ua-platform: "Windows"' -H 'sec-fetch-dest: empty' -H 'sec-fetch-mode: cors' -H 'sec-fetch-site: same-origin' -H 'sec-gpc: 1' -H 'session_uuid: 8cf363d7-65b9-4ca5-bb42-ade63e74f072' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' -H 'web_app_version: 1008010016' -H 'x-age-consent-granted: false'""")
    curl_command = curl_command_template.safe_substitute(date=dateCode)
    # Execute the curl command using subprocess
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True, encoding='utf-8', shell=True)
        print("Curl command executed successfully.", result.stdout)
        # Log the curl command output with timestamp
        logger.info(f"{result.stdout}")
        
        data = json.loads(result.stdout)
        # Fix the walrus operator issue
        first_value = get_nested_value(data, ['response', 'snippets', 7, 'data', 'inventory'])
        stocks = first_value if first_value is not None else get_nested_value(data, ['response', 'snippets', 6, 'data', 'inventory'])
        
        if stocks > 0:
            message = f"Carbona noodles are in stock! Sending message..."
            print(message)
            logger.info(message)
            send_message(dateCode)
        else:
            message = f"Carbona noodles are out of stock."
            print(message)
            logger.info(message)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        logger.error(error_message)
        error_handler()

# Main loop that calls the API every 30 seconds
def main():
    # Set your dateCode here
    dateCode = "20250802"  # You can modify this dynamically as per requirement
    
    logger.info("Starting Blinkit Bot")
    while True:
        message = f"Checking stock status..."
        print(message)
        logger.info(message)
        check_showtimes(dateCode)
        
        # Wait for 30 seconds before calling again
        time.sleep(30)

if __name__ == "__main__":
    main()
