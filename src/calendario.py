
#%%
from ics import Calendar as read_ics 
import requests

import arrow
from datetime import datetime
import time
import urllib.parse


url = 'https://easyacademy.unitn.it/AgendaStudentiUnitn/index.php?view=easycourse&include=corso&txtcurr=1+-+Computational+and+theoretical+modelling+of+language+and+cognition&anno=2023&corso=0708H&anno2%5B%5D=P0407%7C1&date=14-09-2023&_lang=en&highlighted_date=0&_lang=en&all_events=1&'



# from url of easyroom tu  ics uri 
def get_ics_uri(url):
    time.sleep(0.1)  # delay for 100 milliseconds
    uri = urllib.parse.urlparse(url)
    time.sleep(0.1)
    old_search = urllib.parse.parse_qs(uri.query)
    new_uri = urllib.parse.ParseResult(
        scheme="https", 
        netloc="easyacademy.unitn.it", 
        path="/AgendaStudentiUnitn/export/ec_download_ical_list.php", 
        params="", query="", fragment="")

    if old_search["include"][0] == "corso":
        new_query = {
            "include": "corso",
            "anno": old_search["anno"][0],
            "corso": old_search["corso"][0],
            "anno2[]": old_search["anno2[]"][0],
        }

    else:
        final_uri = "URL non riconosciuto"
        

    new_uri = new_uri._replace(query=urllib.parse.urlencode(new_query))
    final_uri = new_uri.geturl() + "&dummyext.ics"  # needed for gnome-calendar and other programs that require an .ics extension
    final_uri
    return final_uri

# an event in the calendar
class Event:
    
    def __init__(self, name, begin, end) -> None:
        # begin and end are datetime objects
        self.name = name
        self.begin = begin
        self.end = end

    def __str__(self) -> str:
        return f"{self.name} from {self.begin} to {self.end}"
    
    def __repr__(self) -> str:
        return f"event  {self.begin}"


class Calendar:

    def __init__(self, ics_uri) -> None:
        self.events = []
        self.parse_ics(get_ics_uri(ics_uri))
    


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
        
        print('calendar parsed', len(self.events))

        return self
    


