
import http.client
import json
import re
from codecs import encode
from datetime import datetime, timedelta
from fake_useragent import UserAgent




BOUNDARY = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
HEADERS = {
    #'User-Agent': 'PostmanRuntime/7.6.1', #added fake_agent so need for now
    "x-forwarded-proto": "https",
    
    'x-requested-with': 'XMLHttpRequest',
    'Cookie': '__cf_bm=NF9eSYEUWmtdv65CHwB93hCdT.WRE_d4iNpmR30o.v0-1676294618-0-AYM6y0RiHGfESmbt61eiam4R1NBuFibW2W71ttdOuSTBogFDoXSTzd07IUeFSNYaM4hNA9R5252aklB7z4C65q8=; firstUdid=0; smd=cb703e1968c6d724ea9d4228e82600fa-1676294628; udid=cb703e1968c6d724ea9d4228e82600fa; PHPSESSID=4qn4pjpfu2a2evaa9n86nv8fph; __cflb=02DiuGRugds2TUWHMkimMbdK71gXQtrnhM92GyeHyjJnY',
    'Content-type': 'multipart/form-data; boundary={}'.format(BOUNDARY)
}

ua = UserAgent()
user_agent = ua.random
HEADERS['User-Agent'] = user_agent
print(HEADERS['User-Agent'], "HEADERS['User-Agent']")


def add_form_data(name: str, value: str) -> []:
    result = []
    result.append(encode('--' + BOUNDARY))
    result.append(encode(f'Content-Disposition: form-data; name={name};'))
    result.append(encode('Content-Type: {}'.format('text/plain')))
    result.append(encode(''))
    result.append(encode(f"{value}"))
    return result

def construct_request(page: int = 0):
    data_list = []
    #today_date = datetime.today().date()
    #date_after_59_days = today_date + timedelta(days=59)
    #date_after_91_days = today_date + timedelta(days=91)
    date_after_59_days = '2024-07-30'
    date_after_91_days = '2024-08-30'
    
    #print("Today's Date -- ", today_date)
    print("Day after 59 days -- ", date_after_59_days)
    print("Day after 91 days -- ", date_after_91_days)
    data_list.extend(add_form_data('dateFrom', str(date_after_59_days)))
    data_list.extend(add_form_data('dateTo', str(date_after_91_days)))
    data_list.extend(add_form_data('currentTab', 'custom'))
    #data_list.extend(add_form_data('limit_from', str(2)))
    data_list.append(encode(''))
    #print(data_list)

    return b'\r\n'.join(data_list)

payload = construct_request(0)

conn = http.client.HTTPSConnection("www.investing.com")

conn.request("POST", "/holiday-calendar/Service/getCalendarFilteredData", payload, HEADERS)
res = conn.getresponse()
data = res.read()   
#print(data.decode("utf-8"), "TST")
json_data = data.decode("utf-8")
parsed_json = json.loads(json_data)
html_content = parsed_json['data']
# Clean the HTML tags and unwanted characters
cleaned_data = html_content.replace('\\/', '/').replace('\\"', '"').replace('<\\/td>', '').replace('<\\/tr>', '').replace('&nbsp;', ' ').strip()
print(cleaned_data, 'cleaned_data') 
#pattern = r'<td class="date bold center">(.*?)<\/td>.*?<span class="float_lang_base_1 ceFlags (.*?)">.*?<\/span><a href="\/markets\/(.*?)">(.*?)<\/a>.*?<td>(.*?)<\/td>.*?<td class="last">(.*?)<\/td>'
#pattern = r'<td class="date bold center">(.*?)</td>\s*<td.*?>(.*?)</a></td>\s*<td>(.*?)</td>\s*<td class="last">(.*?)</td>'
#main
#pattern = r'<td class="date bold center">(.*?)<\/td>.*?<a href="\/markets\/(.*?)">(.*?)<\/a>.*?<td>(.*?)<\/td>.*?<td class="last">(.*?)<\/td>'
pattern = r'<tr>\s*<td class="date bold center">(.*?)<\/td>\s*<td.*?>(?:<span class="float_lang_base_1 ceFlags .*?">.*?<\/span>)?(?:<a href="[^"]*">)?(.*?)(?:<\/a>)?<\/td>\s*<td>(.*?)<\/td>\s*<td class="last">(.*?)<\/td>\s*<\/tr>'
matches = re.findall(pattern, cleaned_data)


#print(matches, "matches")

count = 0
old_date  = None

for match in matches:
    date = match[0].strip()
    if date:
        old_date = date
    else:
        date = old_date
    count += 1  
    country = match[1].strip()
    exchange = match[2].strip()
    event = match[3].strip()

    print(f"Date: {date}, Country: {country}, Exchange: {exchange}, Event: {event}")
print(count, "counted")




"""
import requests
from datetime import datetime, timedelta

HEADERS = {
    'User-Agent': 'PostmanRuntime/7.30.1',
    'x-requested-with': 'XMLHttpRequest',
    'Cookie': '__cf_bm=NF9eSYEUWmtdv65CHwB93hCdT.WRE_d4iNpmR30o.v0-1676294618-0-AYM6y0RiHGfESmbt61eiam4R1NBuFibW2W71ttdOuSTBogFDoXSTzd07IUeFSNYaM4hNA9R5252aklB7z4C65q8=; firstUdid=0; smd=cb703e1968c6d724ea9d4228e82600fa-1676294628; udid=cb703e1968c6d724ea9d4228e82600fa; PHPSESSID=4qn4pjpfu2a2evaa9n86nv8fph; __cflb=02DiuGRugds2TUWHMkimMbdK71gXQtrnhM92GyeHyjJnY'
}

def get_calendar_data():
    try:
        today_date = datetime.today().date()
        date_after_60_days = today_date + timedelta(days=60)
        date_after_90_days = today_date + timedelta(days=90)
        payload = {
            'dateFrom': date_after_60_days,
            'dateTo': date_after_90_days,
            'currentTab': 'custom'
        }
        response = requests.post("https://www.investing.com/holiday-calendar/Service/getCalendarFilteredData", headers=HEADERS, data=payload)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching calendar data: {e}")
        return None

def parse_calendar_data(html_content):
    try:
        pattern = r'<tr>\s*<td class="date bold center">(.*?)<\/td>\s*<td class="bold cur"><span class="float_lang_base_1 ceFlags .*?">&nbsp;<\/span><a href="\/markets\/.*?">(.*?)<\/a><\/td>\s*<td>(.*?)<\/td>\s*<td class="last">(.*?)<\/td>\s*<\/tr>'
        matches = re.findall(pattern, html_content)
        print("Matches:", matches)
        for match in matches:
            yield tuple(field.strip() for field in match)
    except Exception as e:
        print(f"Error parsing calendar data: {e}")
        yield None

def main():
    html_content = get_calendar_data()
    print("HTML Content:", html_content)
    if html_content:
        for date, country, exchange, event in parse_calendar_data(html_content):
            print(f"Date: {date}, Country: {country}, Exchange: {exchange}, Event: {event}")
    else:
        print("Failed to fetch calendar data.")

if __name__ == "__main__":
    main()


"""
