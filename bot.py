import os
import json
import random
from twikit import Client

print("쿠키 로그인 중...")

client = Client()

cookies = json.loads(os.environ["TWITTER_COOKIES"])
client.set_cookies(cookies)

print("로그인 성공")

lines = open("quotes.txt", encoding="utf-8").read().splitlines()
tweet = random.choice(lines)

client.create_tweet(text=tweet)

print("트윗 완료:", tweet)
