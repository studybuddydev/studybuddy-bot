
#%%
from ics import Calendar as read_ics 
import requests
from utils import get_ics_uri
import arrow
from datetime import datetime


url = 'https://easyacademy.unitn.it/AgendaStudentiUnitn/index.php?view=easycourse&include=corso&txtcurr=1+-+Computational+and+theoretical+modelling+of+language+and+cognition&anno=2023&corso=0708H&anno2%5B%5D=P0407%7C1&date=14-09-2023&_lang=en&highlighted_date=0&_lang=en&all_events=1&'
ics_uri = get_ics_uri(url)



class Event:
    
    def __init__(self, name, begin, end) -> None:
        # begin and end are datetime objects
        self.name = name
        self.begin = begin
        self.end = datetime

    def __str__(self) -> str:
        return f"{self.name} from {self.begin} to {self.end}"
    
    def __repr__(self) -> str:
        return f"event  {self.begin}"


class Calendar:

    def __init__(self, ics_uri) -> None:
        self.events = []
        self.parse_ics(ics_uri)
    


    def __str__(self) -> str:
        return f"Calendar with {len(self.events)} events"
    
    def __repr__(self) -> str:
        return f"Calendar with {len(self.events)} events"
    


    def add_event(self, event):
        self.events.append(event)

    def parse_ics(self, ics_uri):
        c = read_ics(requests.get(ics_uri).text)

        for event in c.events:
            self.add_event(Event(event.name, event.begin, event.end))

        return self
    



c = Calendar(ics_uri)
# %%


arrow.utcnow().to("Europe/Rome")