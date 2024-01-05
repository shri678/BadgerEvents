import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import datetime


def configure():
    load_dotenv()


'''
Search for madison events: 
https://app.ticketmaster.com/discovery/v2/events.json?dmaId=328&sort=date,asc&apikey={os.getenv('api_key')}

'''
def ticketmaster_data(session):
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?dmaId=328&sort=name,desc&apikey={os.getenv('api_key')}"
    r = session.get(url)
    return r.json()
    

'''
Get the dates of this month
'''
def dates():
    num_days = 31 #Want data for the next 1 month
    dates = []

    for day in range(num_days):
        cur_day = datetime.date.today() + datetime.timedelta(days=day)
        dates.append(cur_day)
    return dates


'''
Returns data in an array of tuples in the format (title, time, location) for the next month starting
from today's date
'''
def wisc_calendar():
    events_info = []
    dates = dates()

    for date in dates:
        url = f'https://today.wisc.edu/events/day/{date}' #Can change the date to be whatever

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        events = soup.find_all('div', class_='event-details')

        for event in events:

            title = event.find('h3', class_="event-title").text.strip()
            time = None
            location = None

            # Time is all-day
            if event.find('p', class_="event-time") == None:
                time = "All day"
            else:
                time = event.find('p', class_="event-time").text.strip()

            #Location specified
            if event.find('p', class_="event-location") == None:
                location = None
            else:
                location = event.find('p', class_="event-location").text.strip()

            event_tuple = (title, time, location)
            events_info.append(event_tuple)

    return events_info



if __name__ == '__main__':
    configure()
    s = requests.Session()

    events_wisc = wisc_calendar()
    print(events_wisc)


