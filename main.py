import requests
import yfinance as yf
import schedule
import time
from telegram.ext import Updater, CommandHandler

# =========================
# CONFIG
# =========================

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
NEWS_API = "YOUR_NEWS_API"

# =========================
# TELEGRAM
# =========================

updater = Updater(BOT_TOKEN, use_context=True)
bot = updater.bot

# =========================
# LIVE MARKET DATA
# =========================

def get_index_price(symbol):
    try:
        data = yf.Ticker(symbol)
        hist = data.history(period="1d")

        price = round(hist["Close"].iloc[-1], 2)
        return price

    except:
        return "N/A"

# =========================
# MARKET REPORT
# =========================

def get_market_report():

    nifty = get_index_price("^NSEI")
    banknifty = get_index_price("^NSEBANK")
    sensex = get_index_price("^BSESN")

    text = f"""
📈 INDIAN MARKET REPORT

🔹 NIFTY : {nifty}
🔹 BANKNIFTY : {banknifty}
🔹 SENSEX : {sensex}

🟢 MARKET MOOD : RISK ON
🟢 FIIs : BUYING
🟢 DIIs : SUPPORTIVE

⚠️ Follow Risk Management
⚠️ Avoid Overtrading
"""

    return text

# =========================
# MARKET NEWS
# =========================

def get_market_news():

    url = f"https://newsapi.org/v2/top-headlines?category=business&country=in&apiKey={NEWS_API}"

    response = requests.get(url)
    data = response.json()

    articles = data["articles"][:5]

    news = "\n📰 TOP MARKET NEWS\n\n"

    for i, article in enumerate(articles, start=1):

        title = article["title"]

        news += f"{i}. {title}\n\n"

    return news

# =========================
# SEND REPORT
# =========================

def send_daily_report():

    try:

        report = get_market_report()
        news = get_market_news()

        final_message = report + "\n" + news

        bot.send_message(chat_id=CHAT_ID, text=final_message)

        print("REPORT SENT")

    except Exception as e:

        print("ERROR:", e)

# =========================
# COMMANDS
# =========================

def start(update, context):

    msg = """
🔥 PROFESSIONAL MARKET BOT 🔥

Commands:

/news
/nifty
/banknifty
/sensex
/help
"""

    update.message.reply_text(msg)

# =========================

def news(update, context):

    report = get_market_report()
    market_news = get_market_news()

    final = report + "\n" + market_news

    update.message.reply_text(final)

# =========================

def nifty(update, context):

    price = get_index_price("^NSEI")

    update.message.reply_text(f"📈 NIFTY LIVE : {price}")

# =========================

def banknifty(update, context):

    price = get_index_price("^NSEBANK")

    update.message.reply_text(f"🏦 BANKNIFTY LIVE : {price}")

# =========================

def sensex(update, context):

    price = get_index_price("^BSESN")

    update.message.reply_text(f"📊 SENSEX LIVE : {price}")

# =========================

def help_command(update, context):

    help_text = """
📌 AVAILABLE COMMANDS

/news
/nifty
/banknifty
/sensex
/help
"""

    update.message.reply_text(help_text)

# =========================
# HANDLERS
# =========================

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("news", news))
dispatcher.add_handler(CommandHandler("nifty", nifty))
dispatcher.add_handler(CommandHandler("banknifty", banknifty))
dispatcher.add_handler(CommandHandler("sensex", sensex))
dispatcher.add_handler(CommandHandler("help", help_command))

# =========================
# AUTO REPORT SCHEDULE
# =========================

schedule.every().day.at("09:00").do(send_daily_report)

# =========================
# START BOT
# =========================

print("🚀 PROFESSIONAL MARKET BOT RUNNING...")

updater.start_polling()

send_daily_report()

while True:

    schedule.run_pending()

    time.sleep(5)
