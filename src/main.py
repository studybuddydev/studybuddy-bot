#%%
import pandas as pd 
from utils import get_daily_events
from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext
from telegram.ext import filters, MessageHandler

from database_helper import Database

from calendario import Calendar
import schedule
from datetime import datetime
import pytz
import time
import asyncio


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WAITING_FOR_URL = 1


db = Database(os.getenv("DB_PATH"))

db.create_table('users', 'user_id INTEGER, username TEXT, timestamp TEXT')
db.create_table('events', 'id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, begin DATETIME, end DATETIME')

# loggin things
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def send_daily_events(context):
    u = get_daily_events(db)

    for user_id, events in u.items():
        # sort events by start time
        events.sort(key=lambda x: x[1])

        msg = 'LE LEZIONI DI OGGI SONO: \n\n'

        for (event, start, end ) in events:
            msg += f"You have {event} \n  {start} \n  {end} \n\n"

        await context.bot.send_message(
            chat_id=user_id,
            text=msg
        )



 
#%%
# function that should be run at the start of the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # get user id and username
    user_id = update.effective_user.id
    username = update.effective_user.username
    timestamp = update.message.date

    db.execute_query(
        'INSERT INTO users (user_id, username, timestamp) VALUES (?, ?, ?)',
        (user_id, username, timestamp)
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )

    await send_daily_events(context)




def save_calendar(calendar, user_id):
    for event in calendar.events:
        print(event)
        db.execute_query(
            'INSERT INTO events (user_id, name, begin, end) VALUES (?, ?, ?, ?)',
            (user_id, event.name, event.begin.datetime, event.end.datetime)
        )


# function that should be run at the command /addcalendar

async def ask_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # get user id and username
    # send a message asking for calendar url
    print('chiedo url')
    await update.message.reply_text('Please send me the url of your calendar')
    return WAITING_FOR_URL
    #wait for the message

async def receive_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('ricevo url')
    url = update.message.text
    print(url)

    c = Calendar(url)

    save_calendar(c, update.effective_user.id)

    return ConversationHandler.END

def addcalendar_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('addcalendar', ask_url)],
        states={
            WAITING_FOR_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_url)]
        },
        fallbacks=[],
    )

async def send_message():
    userid = 529895213
    application.bot.send_message(
        chat_id=userid,
        text="Hello world"
    )

# run the send message function every 3 seconds 





async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=update.message.tex
    )

def job():
    # get the current time
    now = time.localtime()
    context  = CallbackContext()

    print('job running')

        # run the send_daily_events function
    asyncio.run(send_daily_events(context))

# schedule the job to run every minute
schedule.every().minute.do(job)


async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id='529895213', text='One message every minute')





if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()


    
    start_handler = CommandHandler('start', start) # start command 
    application.add_handler(start_handler)

    addcalendar_handler = addcalendar_handler()
    application.add_handler(addcalendar_handler)

    job_queue = application.job_queue


   
    job_minute = job_queue.run_repeating(send_daily_events, interval=60, first=10)

    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo) # repeat everything
    application.add_handler(echo_handler)

    
    application.run_polling()


# %%




