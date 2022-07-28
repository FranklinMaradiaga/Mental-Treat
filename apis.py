import requests

def activity_generator():
    url = "http://www.boredapi.com/api/activity"
    data = requests.get(url)
    print(data.json()['activity'])
    print(data.json()['type'])

def get_daily_quote():
    url = "https://zenquotes.io/api/today"
    data = requests.get(url)
    print(data.json()[0]['q'])
    print(data.json()[0]['a'])

def get_kanye_quotes():
    url = "https://api.kanye.rest/"
    data = requests.get(url)
    print(data)
    print(data.json()['quote'])


print("\n")
activity_generator()
print("\n\n")
get_daily_quote()
print("\n\n")
get_kanye_quotes()
