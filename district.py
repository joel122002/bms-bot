import time
import json
import subprocess
from string import Template
from utils import get_nested_value, extract_values_by_key, contains_substring, send_message, get_logger

# Get logger for this module
logger = get_logger('district_bot')

def check_showtimes(dateCode):
    curl_command_template = Template(r"""curl 'https://www.district.in/gw/consumer/movies/v3/cinema?meta=1&reqData=1&version=3&site_id=1&channel=web&child_site_id=1&platform=district&cinemaId=57700&date=$date' -H 'accept: */*' -H 'accept-language: en-US,en;q=0.9,ar;q=0.8' -H 'api_source: district' -H 'cache-control: no-cache' -b 'AKA_A2=A; ak_bmsc=0D1E1548C6E14035032C940AA677A069~000000000000000000000000000000~YAAQfwQsF7VEKxOYAQAA3VG5TxzmyZ6NPMU+Uu0Wu8w/8SIHcmHSJCv75q8PT1oiF+fgJ/wIpBx0D2MI+sPITGx3iWnABCVWUOevC6ChhVuwTw6tXAxfCZb7BRQPSkrSmvXJZbBCf4tkNzkm5FABOhby+27Lj7nCN+a/qRztUAOFxl13I3Ot3CsunKBEQfUkkCSfOjSdq+oyPjbMF4wC2qmRvtP3bksoOkF7cDBnB5sYCzjY4UP9HwzPLDx6Vy212zCIv58sDqytM8VW7LhIwYqn1jcg1az0BqT9vRn2J7BrjHyRucBorghz53eLTkzpicZbw4W3jdMWN2B2a8XEPkuCWjsjcMvv13FU/uKjsRqUmm6QkR/hlkyGJzcPvCWuR3FPvpw20XV+tUL9a9LpKA==; x-device-id=7203c3f0-78bc-4616-90a1-c75fc45ce3b8; userProfile=; _gcl_au=1.1.1756327275.1753684204; _fbp=fb.1.1753684204056.761257637277789646; _ga=GA1.1.67911163.1753684204; location=%7B%22id%22%3A3%2C%22title%22%3A%22Mumbai%22%2C%22lat%22%3A19.128567073099326%2C%22long%22%3A72.87749886851958%2C%22subtitle%22%3A%22Maharashtra%22%2C%22cityId%22%3A3%2C%22cityName%22%3A%22Mumbai%22%2C%22pCityId%22%3A%2220%22%2C%22pCityKey%22%3A%22mumbai%22%2C%22pCityName%22%3A%22Mumbai%22%2C%22pStateKey%22%3A%22maharashtra%22%2C%22pStateName%22%3A%22Maharashtra%22%2C%22placeType%22%3A%22GOOGLE_PLACE%22%2C%22placeId%22%3A%22ChIJE6xvrR_I5zsRalYN9TPYB9M%22%2C%22countryId%22%3A%221%22%2C%22subzoneId%22%3A%222117%22%7D; _rdt_uuid=1753684203989.8843b383-85f5-4848-a7ca-fd8718b8a29a; _ga_KHRD29M2W7=GS2.1.s1753684204$o1$g1$t1753684279$j54$l0$h663047942; _ga_WDEHDQ2ZK7=GS2.1.s1753684204$o1$g1$t1753684279$j54$l0$h1182453178; RT="z=1&dm=www.district.in&si=6790ed5e-2ace-4c37-bcc9-f69aa693e501&ss=mdmqamvx&sl=1&tt=1q9&rl=1&nu=3bu3480f&cl=1qwu"; _dd_s=aid=93cbd2c9-9e17-415d-921c-0deae4cba8cc&logs=1&id=f286a77c-b6df-4dac-bee2-909b60c0fc23&created=1753684203564&expire=1753685184125&rum=1; bm_sv=3D1B73EA341AE10D5C8666F50727151A~YAAQLxzFF9D/HBWYAQAA5pK6TxwbOMrscGgoJ9cnMdJhbhGVor1itXnDm/zwAAx1koNOEGsPSwgSW5lBufLnMvecuclcK4R1RvRgqblzcZYEadunNRqnWn/+oR7LX6WpK8rHqqzmJ39oZNGG5zl5cZU8tIwCDgwnC4j3Ds9Vvg92WcTfR4ESJ2BNLVUFdAkionKAls5z4G1FXp9aRMUuvM1kLm8ISPyU7uvvQ7KteU7QcUDPmDOsdwt6+Se9vEdsnkI=~1' -H 'pragma: no-cache' -H 'priority: u=1, i' -H 'referer: https://www.district.in/movies/cinepolis-nexus-seawoods-navi-mumbai-in-mumbai-CD57700?fromdate=2025-07-30' -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"' -H 'sec-ch-ua-mobile: ?0' -H 'sec-ch-ua-platform: "Windows"' -H 'sec-fetch-dest: empty' -H 'sec-fetch-mode: cors' -H 'sec-fetch-site: same-origin' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' -H 'x-app-type: ed_web' -H 'x-guest-token: 1753684284205_775645867272472700_yzbj6loinsk'""")
    curl_command = curl_command_template.safe_substitute(date=dateCode)
    # Execute the curl command using subprocess
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True, encoding='utf-8', shell=True)
        print("Curl command executed successfully.", result.stdout)
        # Log the curl command output with timestamp
        logger.info(f"{result.stdout}")
        
        data = json.loads(result.stdout)
        movies = get_nested_value(data, ['meta', 'movies'])
        names = extract_values_by_key(movies, "label")
        if contains_substring(names, "Slayer"):
            message = f"DateCode {dateCode} matches! Sending message..."
            print(message)
            logger.info(message)
            send_message(dateCode)
        else:
            message = f"DateCode {dateCode} does not match."
            print(message)
            logger.info(message)
    except subprocess.CalledProcessError as e:
        error_message = f"Failed to execute curl command. Error: {e}"
        print(error_message)
        logger.error(error_message)
    except UnicodeDecodeError as e:
        error_message = f"Unicode decode error: {e}"
        print(error_message)
        logger.error(error_message)

# Main loop that calls the API every 30 seconds
def main():
    # Set your dateCode here
    dateCode = "2025-09-13"  # You can modify this dynamically as per requirement
    
    logger.info("Starting District Bot")
    while True:
        print(f"Checking showtimes for {dateCode}...")
        logger.info(f"Checking showtimes for {dateCode}")
        check_showtimes(dateCode)
        
        # Wait for 30 seconds before calling again
        time.sleep(30)

if __name__ == "__main__":
    main()
