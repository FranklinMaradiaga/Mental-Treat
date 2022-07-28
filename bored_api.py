import requests

def activity_generator():
    url = "http://www.boredapi.com/api/activity"
    data = requests.get(url)
    print(data.json()['activity'])
    print(data.json()['type'])

def get_daily_quote():
    url = "https://zenquotes.io/api/today"


activity_generator()
get_daily_quote()