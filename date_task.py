from datetime import datetime, timedelta
today_date = datetime.today().date()
date_after_60_days = today_date + timedelta(days=60)
print(today_date)