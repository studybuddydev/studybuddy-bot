#%%
import pandas as pd 
from utils import get_ics_uri
from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
#%%
# loggin things
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# function that should be run at the start of the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )




async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=update.message.tex
    )

    



if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    
    application.run_polling()
# %%

url = 'https://easyacademy.unitn.it/AgendaStudentiUnitn/index.php?view=easycourse&include=corso&txtcurr=1+-+Computational+and+theoretical+modelling+of+language+and+cognition&anno=2023&corso=0708H&anno2%5B%5D=P0407%7C1&date=14-09-2023&_lang=en&highlighted_date=0&_lang=en&all_events=1&'
get_ics_uri(url)


# %%
