import requests
import schedule
import time

BOT_TOKEN = "8268514632:AAFnUdnuodljVYJCC12MF1-wWMFNE1AeS50"
CHAT_ID = "5508263164"
NEWS_API = "e417c06afa274a45865f957526a6d10b"

# SEND MESSAGE
def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url, data=payload)

# GET NEWS
def get_news():

    try:

        url = f"https://newsapi.org/v2/top-headlines?category=business&country=us&apiKey={NEWS_API}"

        response = requests.get(url)

        data = response.json()

        articles = data["articles"][:5]

        news = "📊 TOP MARKET NEWS\n\n"

        for i, article in enumerate(articles, start=1):

            news += f"{i}. {article['title']}\n\n"

        return news

    except Exception as e:

        return f"News Error: {e}"

# DAILY REPORT
def send_report():

    report = """
📈 INDIAN MARKET REPORT

🔹 NIFTY : Bullish
🔹 BANKNIFTY : Strong
🔹 MARKET MOOD : Risk ON
🔹 FIIs : Buying
🔹 DIIs : Supportive

⚠️ Follow Risk Management
⚠️ Avoid Overtrading
"""

    news = get_news()

    final = report + "\n\n" + news

    send_message(final)

# START MESSAGE
send_message("🔥 MARKET BOT STARTED SUCCESSFULLY 🔥")

send_report()

# DAILY AUTO UPDATE
schedule.every().day.at("09:00").do(send_report)

print("🚀 BOT RUNNING...")

# LOOP
while True:

    schedule.run_pending()

    time.sleep(5)