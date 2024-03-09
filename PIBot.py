import asyncio
import datetime
import time
import schedule
from telegram import Bot
from datetime import datetime, timezone, timedelta
import requests
import json
BOT_TOKEN = ''
CHAT_ID = ''
bot = Bot(token=BOT_TOKEN)

def send_telegram_message(message):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.send_message(chat_id=CHAT_ID, text=message))


def fetch_premium_index():
    endpoint = 'https://www.binance.com/fapi/v1/marketKlines'
    
    params = {
        'symbol': 'pBTCUSDT',
        'interval': '1m'
    }
    
    # Make the GET request to the Binance API
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        klines = response.json()
        high_index = float(klines[-2][2])
        average_of_klines = sum(float(kline[2]) for kline in klines[-32:-2]) / 30
        
        print(f"High Index: {high_index*100}%, Average of the selected Klines: {average_of_klines*100}%")
        if (high_index - average_of_klines) > 0.0003 :
            send_telegram_message(f'Alert: High Index {high_index*100}% is 0.3 more than the average {average_of_klines*100}% of the selected Klines.')
        low_index = float(klines[-2][3])
        average_of_klines_low = sum(float(kline[3]) for kline in klines[-32:-2]) / 30
        
        print(f"Low Index: {low_index*100}%, Average of the selected Klines: {average_of_klines_low*100}%")

        if (low_index - average_of_klines_low) < -0.0003 :
            send_telegram_message(f'Alert: Low Index {low_index*100}% is 0.3 less than the average {average_of_klines_low*100}% of the selected Klines.')
    else:
        print(f"Failed to fetch data: Status code {response.status_code}")
fetch_premium_index()
def job():
    now = datetime.now()
    print(f"Fetching Premium Index at {now.strftime('%Y-%m-%d %H:%M:%S')}")
    fetch_premium_index()

while True:
    current_time = datetime.now()
    if current_time.second == 10:
        job()
        time.sleep(59)
    else:
        time.sleep(0.5)
