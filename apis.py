import requests

def activity_generator():
    url = "http://www.boredapi.com/api/activity"
    data = requests.get(url)
    return data.json()['activity']

def get_daily_quote():
    url = "https://zenquotes.io/api/today"
    data = requests.get(url)
    return data.json()[0]['q']

def get_author():
    url = "https://zenquotes.io/api/today"
    data = requests.get(url)
    return data.json()[0]['a']

def get_kanye_quote():
    url = "https://api.kanye.rest/"
    data = requests.get(url)
    return (data.json()['quote'])

print("\n\n", get_kanye_quote())

