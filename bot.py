import random
from twikit import Client

USERNAME = "@Ren_k107"
EMAIL = "chomm1313@gmail.com"
PASSWORD = "znfhtkdhkfps000"

client = Client()

client.login(
    auth_info_1=USERNAME,
    auth_info_2=EMAIL,
    password=PASSWORD
)

with open("quotes.txt", "r", encoding="utf-8") as f:
    quotes = f.readlines()

tweet = random.choice(quotes).strip()

client.create_tweet(text=tweet)

print("tweet:", tweet)
