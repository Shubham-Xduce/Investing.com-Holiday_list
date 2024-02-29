import requests
from openpyxl import Workbook

# Define the URL to hit
url = "https://in.investing.com/holiday-calendar/Service/getCalendarFilteredData"


headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://in.investing.com/holiday-calendar/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}
cookies = {
    "PHPSESSID": "7j9kvmpub0r86v7i1cqfsjq3ui",
    "geoC": "IN",
    # Add more cookies as needed
}
payload = {
    'dateFrom': '2024-02-27',
    'dateTo': '2024-05-28',
    'country': '',
    'currentTab': 'custom',
    'limit_from': 0
    }

# Define your payload if any

response = requests.post(url, headers=headers, cookies=cookies, data=payload)

print(response.status_code)
print(response.text)  # Response content
# Define the payload for the POST request

# Send the POST request
response = requests.post(url, data=payload)
print(response.status_code, dir(response), response.request)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response data
    response_data = response.json()  # Assuming the response is in JSON format

    # Create a new Excel workbook
    workbook = Workbook()
    sheet = workbook.active

    # Write the response data to the Excel sheet
    for index, data in enumerate(response_data):
        sheet.cell(row=index+1, column=1, value=data)

    # Save the workbook
    workbook.save("response_data.xlsx")

    print("Data saved to response_data.xlsx")
else:
    print("Failed to retrieve data from the URL")
