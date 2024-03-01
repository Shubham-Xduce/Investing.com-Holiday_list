import http.client
import json
from codecs import encode
import re
from datetime import datetime, timedelta

BOUNDARY = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
HEADERS = {
    'User-Agent': 'PostmanRuntime/7.30.1',
    'x-requested-with': 'XMLHttpRequest',
    'Cookie': '__cf_bm=NF9eSYEUWmtdv65CHwB93hCdT.WRE_d4iNpmR30o.v0-1676294618-0-AYM6y0RiHGfESmbt61eiam4R1NBuFibW2W71ttdOuSTBogFDoXSTzd07IUeFSNYaM4hNA9R5252aklB7z4C65q8=; firstUdid=0; smd=cb703e1968c6d724ea9d4228e82600fa-1676294628; udid=cb703e1968c6d724ea9d4228e82600fa; PHPSESSID=4qn4pjpfu2a2evaa9n86nv8fph; __cflb=02DiuGRugds2TUWHMkimMbdK71gXQtrnhM92GyeHyjJnY',
    'Content-type': 'multipart/form-data; boundary={}'.format(BOUNDARY)
}

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
    today_date = datetime.today().date()
    date_after_60_days = today_date + timedelta(days=60)
    date_after_90_days = today_date + timedelta(days=90)
    data_list.extend(add_form_data('dateFrom', str(date_after_60_days)))
    data_list.extend(add_form_data('dateTo', str(date_after_90_days)))
    data_list.extend(add_form_data('currentTab', 'custom'))
    #data_list.extend(add_form_data('limit_from', str(2)))

    data_list.append(encode(''))
    return b'\r\n'.join(data_list)

payload = construct_request(0)

conn = http.client.HTTPSConnection("www.investing.com")

conn.request("POST", "/holiday-calendar/Service/getCalendarFilteredData", payload, HEADERS)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"), "TST")
json_data = data.decode("utf-8")
parsed_json = json.loads(json_data)
html_content = parsed_json['data']
# Clean the HTML tags and unwanted characters
cleaned_data = html_content.replace('\\/', '/').replace('\\"', '"').replace('<\\/td>', '').replace('<\\/tr>', '').replace('&nbsp;', ' ').strip()

pattern = r'<td class="date bold center">(.*?)<\/td>.*?<a href="\/markets\/(.*?)">(.*?)<\/a>.*?<td>(.*?)<\/td>.*?<td class="last">(.*?)<\/td>'
matches = re.findall(pattern, cleaned_data, re.DOTALL)

count = 0
for match in matches:
# Process each match to extract event details
    count += 1
    date = match[0].strip()
    country = match[2].strip()
    exchange = match[3].strip()
    event = match[4].strip()
    print(f"Date: {date}, Country: {country}, Exchange: {exchange}, Event: {event}")
print(count, "counted")
# Print the cleaned data
#print(cleaned_data)
"""
# Extracting data without BeautifulSoup
rows = re.findall(r'<tr[^>]*>(.*?)<\/tr>', html_content, re.DOTALL)

count = 0
for row in rows:
    count += 1
    date = re.search(r'<td[^>]*class=\"date bold center\"><\/td>\s*<td[^>]*>([^<]*)<\/td>', row).group(1).strip()
    country = re.search(r'<td[^>]*class=\"bold cur\"><span[^>]*>[^<]*<\/span><a[^>]*>([^<]*)<\/a>', row).group(1).strip()
    exchange = re.search(r'<td[^>]*>([^<]*)<\/td>', row).group(1).strip()
    event = re.search(r'<td[^>]*class=\"last\">([^<]*)<\/td>', row).group(1).strip()

    print(f"Date: {date}, Country: {country}, Exchange: {exchange}, Event: {event}")
"""
#print(count, "total count")
