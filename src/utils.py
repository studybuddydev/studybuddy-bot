
#%%



# %%

import time
import urllib.parse

url = 'https://easyacademy.unitn.it/AgendaStudentiUnitn/index.php?view=easycourse&include=corso&txtcurr=1+-+Computational+and+theoretical+modelling+of+language+and+cognition&anno=2023&corso=0708H&anno2%5B%5D=P0407%7C1&date=14-09-2023&_lang=en&highlighted_date=0&_lang=en&all_events=1&'

def get_ics_uri(url):
    time.sleep(0.1)  # delay for 100 milliseconds
    uri = urllib.parse.urlparse(url)
    old_search = urllib.parse.parse_qs(uri.query)
    new_uri = urllib.parse.ParseResult(scheme="https", netloc="easyacademy.unitn.it", path="/AgendaStudentiUnitn/export/ec_download_ical_list.php", params="", query="", fragment="")

    if old_search["include"][0] == "corso":
        new_query = {
            "include": "corso",
            "anno": old_search["anno"],
            "corso": old_search["corso"],
            "anno2[]": old_search["anno2[]"],
        }

    else:
        final_uri = "URL non riconosciuto"
        

    new_uri = new_uri._replace(query=urllib.parse.urlencode(new_query))
    final_uri = new_uri.geturl() + "&dummyext.ics"  # needed for gnome-calendar and other programs that require an .ics extension
    final_uri
    return final_uri

# %%

# %%
