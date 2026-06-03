import requests
import yfinance as yf
import schedule
import time
from telegram.ext import Updater, CommandHandler

# =========================================
# YOUR CONFIG
# =========================================

BOT_TOKEN = "8268514632:AAFnUdnuodljVYJCC12MF1-wWMFNE1AeS50"
CHAT_ID = "5508263164"
NEWS_API = "e417c06afa274a45865f957526a6d10b"

# =========================================
# TELEGRAM SETUP
# =========================================

updater = Updater(BOT_TOKEN, use_context=True)
bot = updater.bot

# =========================================
# LIVE MARKET DATA
# =========================================

def get_index_price(symbol):

    try:

        ticker = yf.Ticker(symbol)

        hist = ticker.history(period="1d")

        price = round(hist["Close"].iloc[-1], 2)

        return price

    except:

        return "N/A"

# =========================================
# MARKET REPORT
# =========================================

def get_market_report():

    nifty = get_index_price("^NSEI")

    banknifty = get_index_price("^NSEBANK")

    sensex = get_index_price("^BSESN")

    report = f"""
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

    return report

# =========================================
# MARKET NEWS
# =========================================

def get_market_news():

    try:

        url = f"https://newsapi.org/v2/top-headlines?category=business&country=in&apiKey={NEWS_API}"

        response = requests.get(url)

        data = response.json()

        articles = data["articles"][:5]

        news = "\n📰 TOP MARKET NEWS\n\n"

        for i, article in enumerate(articles, start=1):

            title = article["title"]

            news += f"{i}. {title}\n\n"

        return news

    except Exception as e:

        return f"News Error: {e}"

# =========================================
# SEND DAILY REPORT
# =========================================

def send_daily_report():

    try:

        report = get_market_report()

        news = get_market_news()

        final_message = report + "\n" + news

        bot.send_message(chat_id=CHAT_ID, text=final_message)

        print("REPORT SENT SUCCESSFULLY")

    except Exception as e:

        print("ERROR:", e)

# =========================================
# COMMANDS
# =========================================

def start(update, context):

    msg = """
🔥 PROFESSIONAL MARKET BOT 🔥

AVAILABLE COMMANDS:

/news
/nifty
/banknifty
/sensex
/help
"""

    update.message.reply_text(msg)

# =========================================

def news(update, context):

    report = get_market_report()

    market_news = get_market_news()

    final = report + "\n" + market_news

    update.message.reply_text(final)

# =========================================

def nifty(update, context):

    price = get_index_price("^NSEI")

    update.message.reply_text(f"📈 NIFTY LIVE : {price}")

# =========================================

def banknifty(update, context):

    price = get_index_price("^NSEBANK")

    update.message.reply_text(f"🏦 BANKNIFTY LIVE : {price}")

# =========================================

def sensex(update, context):

    price = get_index_price("^BSESN")

    update.message.reply_text(f"📊 SENSEX LIVE : {price}")

# =========================================

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

# =========================================
# HANDLERS
# =========================================

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))

dispatcher.add_handler(CommandHandler("news", news))

dispatcher.add_handler(CommandHandler("nifty", nifty))

dispatcher.add_handler(CommandHandler("banknifty", banknifty))

dispatcher.add_handler(CommandHandler("sensex", sensex))

dispatcher.add_handler(CommandHandler("help", help_command))

# =========================================
# AUTO DAILY REPORT
# =========================================

schedule.every().day.at("09:00").do(send_daily_report)

# =========================================
# START BOT
# =========================================

print("🚀 PROFESSIONAL MARKET BOT RUNNING...")

bot.send_message(chat_id=CHAT_ID, text="🔥 MARKET BOT STARTED SUCCESSFULLY 🔥")

updater.start_polling()

send_daily_report()

while True:

    schedule.run_pending()

    time.sleep(5)
