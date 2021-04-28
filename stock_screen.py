import requests as _requests
import bs4 as _bs4
from typing import List

#returns string
def _generate_url(month: str, day: int):
    url = f"https://www.onthisday.com/day/{month}/{day}"
    return url 

#returns beautiful soup object
def _get_page(url: str):
    page =  _requests.get(url)
    soup = _bs4.BeautifulSoup(page.content, "html.parser")
    return soup

#returns list
def events_of_the_day(month: str, day: int):
    """
    Returns the event of a given day
    """
    url = _generate_url(month, day)
    page = _get_page(url)
    raw_events = page.find_all(class_="event")
    events = [event.text for event in raw_events]
    print(events)
    return events

events_of_the_day("february", 24)


