
#%%



# %%

import time
import urllib.parse
from database_helper import Database
import os
import arrow
import pytz

url = 'https://easyacademy.unitn.it/AgendaStudentiUnitn/index.php?view=easycourse&include=corso&txtcurr=1+-+Computational+and+theoretical+modelling+of+language+and+cognition&anno=2023&corso=0708H&anno2%5B%5D=P0407%7C1&date=14-09-2023&_lang=en&highlighted_date=0&_lang=en&all_events=1&'






def get_daily_events(db):
    now = arrow.utcnow()

    # Calculate the time 30 minutes from now
    reminder_time = now.shift(minutes=-2000)

    user_timezone = pytz.timezone('Europe/Rome')  # Replace with the user's timezone
    reminder_time = reminder_time.to(user_timezone)



    # set time at day 
    reminder_time = reminder_time.replace(hour=8, minute=0, second=0, microsecond=0)

    reminder_time_end = reminder_time.replace(hour=23, minute=59, second=59, microsecond=0)




    events = db.execute_query(
        'SELECT * FROM events WHERE begin BETWEEN ? AND ?',
        (reminder_time.datetime, reminder_time_end.datetime)
    )

    users = {}

    for event in events:
        if event[1] in users:
            users[event[1]].append(event[2:])
        else:
            users[event[1]] = [event[2:]]


    return users
# send message to user with all the lessons of the day







# %%
