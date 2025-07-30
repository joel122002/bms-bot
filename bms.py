import time
import json
import subprocess
from string import Template
from utils import get_nested_value, extract_values_by_key, contains_substring, send_message

def check_showtimes(dateCode):
    curl_command_template = Template(r"""curl_chrome116 'https://in.bookmyshow.com/api/v3/mobile/showtimes/byvenue?dateCode=$date&venueCode=CSWO&regionCode=MUMBAI&memberId=&bmsId=1.685005278.1753847811369&appCode=WEBV2&token=26x3aab5x746514b3b7b&lsId=' -H 'accept: application/json, text/plain, */*' -H 'accept-language: en-US,en;q=0.9' -H 'baggage: sentry-environment=production,sentry-release=release_3796,sentry-public_key=4d17a59c2597410e714ab31d421148d9,sentry-trace_id=cb2bd2a2d64342899f42423e3d73fc71,sentry-transaction=%2Fcinemas%2F%3AregionNameSlug%2F%3AvenueNameSlug%2Fbuytickets%2F%3AvenueCode%2F%3AshowDate%3F,sentry-sampled=false,sentry-sample_rand=0.7810927444382634,sentry-sample_rate=0.001' -H 'cache-control: no-cache' -b '__cfruid=01f5b98f664205015be49b432d07352171a70bbe-1753847811; bmsId=1.685005278.1753847811369; preferences=%7B%22ticketType%22%3A%22M-TICKET%22%7D; _gcl_au=1.1.412415022.1753847813; WZRK_G=483fde3a314d413bbf2a4ea206124452; _ga=GA1.1.307642472.1753847813; _fbp=fb.1.1753847813351.3224693857157380; geoHash=%22%22; geolocation=%7B%22x-location-shared%22%3Afalse%2C%22x-location-selection%22%3A%22manual%22%2C%22timestamp%22%3A1753847820672%7D; AMP_TOKEN=%24NOT_FOUND; tvc_bmscookie=GA1.2.307642472.1753847813; tvc_bmscookie_gid=GA1.2.1997873852.1753847822; cto_bundle=ySakhV9JZEZNbm9ZUmJIM3VWcWNocVlZak1mWjNublY2RnkyZ0s3ZFN6RzNCREs4SkRwcmhWdTAlMkJmekplRUh4Q2VRRGhpQmN0WkJNcDlHJTJGcXMxSm0lMkJCJTJCdkxmZDY3Y0hxJTJGOFlyWWlHUyUyRlZkS1lXVDRuJTJGZzNsa24xQUtFJTJGaXBIVzlFZWI; rgn=%7B%22regionNameSlug%22%3A%22mumbai%22%2C%22regionCodeSlug%22%3A%22mumbai%22%2C%22regionName%22%3A%22Mumbai%22%2C%22regionCode%22%3A%22MUMBAI%22%2C%22subName%22%3A%22%22%2C%22subCode%22%3A%22%22%2C%22Lat%22%3A%2219.076%22%2C%22Long%22%3A%2272.8777%22%2C%22GeoHash%22%3A%22te7%22%7D; mrs=%5B%22CSWO%22%5D; __cf_bm=b5FufDiFWnwankhAfUFTPTTJ2ARw0Gm0X5t6sutw5s0-1753848326-1.0.1.1-7L2xKOwDsewe3TVuzCp6un6Dm4IVdW6YQovs_v3Qgzv6AGud8KPmKtK8wvE5JfakxC2KysAKDLxoIZpTxbRRBhUcUZyEme7bEdVxg6owJ8Y; _cfuvid=I1EerjyGMZ17n2nYDwFPZ3cjkSbxLjCQytM2DK4Ig34-1753848326654-0.0.1.1-604800000; platform=%7B%22segments%22%3A%22%22%7D; _gat_UA-27207583-8=1; WZRK_S_RK4-47R-98KZ=%7B%22p%22%3A6%2C%22s%22%3A1753847812%2C%22t%22%3A1753848328%7D; cf_clearance=07gT4BIokpk7wVFMLz87RKOFKItYm_ZwfGFlNG2Fdck-1753848328-1.2.1.1-5Ufq1Qi3XLud.y4eslmXiiOfmYIcXnL8yJ.qb1WrHSHskv_6qVRnHXvqDJo1vACwsKdKABB1.vruTR2WokP6KVH6IxN_a1s5eP1VJAA8Wb6EQ5ZuEON1r6xxM3ckRWIYx_thJactsl2728BaOOJIhN9DdeZOozmVDTeGfXuVUiMBxc7jTD9qHKR9N_LdBa9xiaFXFvclYQhhRqesgtcqIoAGYY4ncJiSdwZd.iquz60; _ga_84T5GTD0PC=GS2.1.s1753847813$o1$g1$t1753848328$j58$l0$h0' -H 'pragma: no-cache' -H 'priority: u=1, i' -H 'referer: https://in.bookmyshow.com/cinemas/mumbai/cinepolis-nexus-seawoods-nerul-navi-mumbai/buytickets/CSWO/$date' -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"' -H 'sec-ch-ua-mobile: ?0' -H 'sec-ch-ua-platform: "Windows"' -H 'sec-fetch-dest: empty' -H 'sec-fetch-mode: cors' -H 'sec-fetch-site: same-origin' -H 'sentry-trace: cb2bd2a2d64342899f42423e3d73fc71-8fbe5a6e551ac4a2-0' -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' -H 'x-app-code: WEB' -H 'x-region-code: MUMBAI'""")
    curl_command = curl_command_template.safe_substitute(date=dateCode)
    # Execute the curl command using subprocess
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True, encoding='utf-8', shell=True)
        print("Curl command executed successfully.", result.stdout)
        data = json.loads(result.stdout)
        movies = get_nested_value(data, ['ShowDetails', 0, 'Event'])
        date = get_nested_value(data, ['ShowDetails', 0, 'Event'])
        names = extract_values_by_key(movies, "EventTitle")
        if contains_substring(names, "Fantastic") and date == dateCode:
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
    dateCode = "20250802"  # You can modify this dynamically as per requirement
    
    while True:
        print(f"Checking showtimes for {dateCode}...")
        check_showtimes(dateCode)
        
        # Wait for 30 seconds before calling again
        time.sleep(30)

if __name__ == "__main__":
    main()
