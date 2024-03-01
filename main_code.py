import http.client
import json
from codecs import encode
 
from bs4 import BeautifulSoup
 
BOUNDARY = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
HEADERS = {
    'User-Agent': 'PostmanRuntime/7.30.1',
    'x-requested-with': 'XMLHttpRequest',
    'Cookie': '__cf_bm=NF9eSYEUWmtdv65CHwB93hCdT.WRE_d4iNpmR30o.v0-1676294618-0-AYM6y0RiHGfESmbt61eiam4R1NBuFibW2W71ttdOuSTBogFDoXSTzd07IUeFSNYaM4hNA9R5252aklB7z4C65q8=; firstUdid=0; smd=cb703e1968c6d724ea9d4228e82600fa-1676294628; udid=cb703e1968c6d724ea9d4228e82600fa; PHPSESSID=4qn4pjpfu2a2evaa9n86nv8fph; __cflb=02DiuGRugds2TUWHMkimMbdK71gXQtrnhM92GyeHyjJnY',
    'Content-type': 'multipart/form-data; boundary={}'.format(BOUNDARY)
}
 
 
def add_form_data(name: str, value: str) -> []:
    result = []
    # boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
 
    result.append(encode('--' + BOUNDARY))
    result.append(encode(f'Content-Disposition: form-data; name={name};'))
    result.append(encode('Content-Type: {}'.format('text/plain')))
    result.append(encode(''))
    result.append(encode(f"{value}"))
    return result
 
 
def construct_request(page: int = 0):
    data_list = []
 
    #data_list.extend(add_form_data('country[]', '5'))
    #data_list.extend(add_form_data('country[]', '17'))
    #data_list.extend(add_form_data('country[]', '43'))
 
    data_list.extend(add_form_data('dateFrom', '2024-12-01'))
 
    data_list.extend(add_form_data('dateTo', '2024-12-31'))
 
    #data_list.extend(add_form_data('timeZone', '8'))
 
    #data_list.extend(add_form_data('timeFilter', 'timeRemain'))
 
    data_list.extend(add_form_data('currentTab', 'custom'))
 
    #data_list.extend(add_form_data('submitFilters', '1'))
 
    #data_list.extend(add_form_data('limit_from', str(page)))
 
    #data_list.append(encode('--' + BOUNDARY + '--'))
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


print(html_content, "html_content")
soup = BeautifulSoup(html_content, 'html.parser')

rows = soup.find_all('tr')

count=0
for row in rows:
    count+=1
    date = row.find('td', class_='date').text.strip()

    country_tag = row.find('a')
    country = country_tag.text.strip() if country_tag else "Unknown"
    exchange = row.find_all('td')[2].text.strip()
    #event = row.find('td', class_='last').text.strip()
    event = row.find('td', class_='last').text.strip()
    #exchange_tag = row.find('td')
    #exchange = exchange_tag.text.strip() if exchange_tag else ""

    print(f"Date: {date}, Country: {country}, Exchange: {exchange}, Event: {event}")
print(count, "total count")
"""
for row in rows:
    date = row.find('td', class_='date').text.strip()

    country_tag = row.find('a')
    country = country_tag.text.strip() if country_tag else "Unknown"

    event = row.find('td', class_='last').text.strip()

    print(f"Date: {date}, Country: {country}, Event: {event}")



"""
 
json_data = json.loads(data.decode("utf-8"))
# print(json_data)
soup = BeautifulSoup(json_data['data'], 'html.parser')
items = soup.find_all('tr', {"class": "js-event-item"})
print(len(items))
for item in items:
    # country = item.find('td', {"class": "flagCur"})
    # title = item.find('td', {"class": "left event"})
    print(f"{item.text}")