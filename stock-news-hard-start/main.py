import requests
import os
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

account_sid = "AC2d558aa54b39737b6fcc9f5164a70b90"
auth_token = "9ed6d33ccfbb27d2b864f6dacb56829f"
api_key = "51f0a9294ce0915e91fe8a699ba5f905"
fr_phone = +13345092276
to_phone = +306970548924

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
api_key_news = "a3a3be95e3d9416b921dee371a449e99"
api_key_stocks = "FNG1UD53HZM0TSUX"
param_news = {
    "q": COMPANY_NAME,
    "apiKey": api_key_news,
    #"country": "us",
    #"category": "business",
}
param_stocks = {
    "apikey": api_key_stocks,
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
}

new_response = requests.get(url=NEWS_ENDPOINT, params=param_news)
new_response.raise_for_status()
news = new_response.json()["articles"][:3]
titles = []
descriptions = []
for i in news:
    titl = i["title"]
    desc = i["description"]
    titles.append(titl)
    descriptions.append(desc)

stock_response = requests.get(url=STOCK_ENDPOINT, params=param_stocks)
stock_response.raise_for_status()
data = stock_response.json()
data_list = [value for (key, value) in data.items()]
yesterday_closing = float(data_list[0]["4. close"])
before_yesterday = float(data_list[1]["4. close"])
emoji_up = "🔺"
emoji = "🔻"

if yesterday_closing < before_yesterday:
    emoji = emoji_up

difference = abs(yesterday_closing-before_yesterday)
percentage = difference % yesterday_closing
message = f"{STOCK}: {emoji}%{round(percentage)}\nHeadline: {titles[0]}\nBrief: {descriptions[0]}\n" \
          f"{STOCK}: {emoji}%{round(percentage)}\nHeadline: {titles[0]}\nBrief: {descriptions[1]}" \
          f"{STOCK}: {emoji}%{round(percentage)}\nHeadline: {titles[0]}\nBrief: {descriptions[2]}"

if percentage > 5:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=fr_phone,
        to=to_phone
    )
    print(message.status)


