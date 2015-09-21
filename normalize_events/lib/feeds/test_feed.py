from ..event import Event
import datetime

class TestClient(object):
    def __init__(self):
        pass

    def get_events(self):
        test_event = Event()
        test_event.address1 = "2112 N Ashland Ave"
        test_event.address2 = "Sushi Bar"
        test_event.api = "https://www.eventbriteapi.com/v3/events/16560763690/?token=WCK2NEHVAHMTNGVJYIM7"
        test_event.city = "Chicago"
        test_event.cost = 15.0
        test_event.created = "Tue, 21 Apr 2015 23:48:38 GMT"
        test_event.date = datetime.datetime.strptime('Jul 15 2015', '%b %d %Y')
        test_event.day = "Wednesday"
        test_event.description = "Join us at Mariano's Bucktown for a sushi rolling and sake/beer tasting class!"
        test_event.id = 7
        test_event.link = "http://www.eventbrite.com/e/sushi-rolling-sake-tasting-tickets-16560763690?aff=ebapi"
        test_event.month = "July"
        test_event.name = "Sushi Rolling & Sake Tasting"
        test_event.place = "Mariano's Bucktown"
        test_event.state = "IL"
        test_event.suburbs = False
        test_event.time = "06:30 PM"
        test_event.year = "2015"
        test_event.zipcode = "60614"
        test_event.source = 'Brown Paper Tickets'
        test_event.api_id = '1784315'
        return [test_event]
