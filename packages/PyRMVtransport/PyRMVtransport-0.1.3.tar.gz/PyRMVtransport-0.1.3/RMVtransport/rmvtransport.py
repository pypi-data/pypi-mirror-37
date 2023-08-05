"""A module to query bus and train departure times."""
import asyncio
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import html
import json
import logging
import aiohttp
import async_timeout
from lxml import objectify
from lxml import etree


PRODUCTS = {
    'ICE': 1,
    'IC': 2,
    'EC': 2,
    'RB': 4,
    'RE': 4,
    'S': 8,
    'U-Bahn': 16,
    'Tram': 32,
    'Bus': 64,
    'Bus2': 128,
    'Fähre': 256,
    'Taxi': 512,
    'Bahn': 1024,
}
ALL = PRODUCTS.keys()

_LOGGER = logging.getLogger(__name__)


class RMVtransportError(Exception):
    """General RMV transport error exception occurred."""

    pass


class RMVtransportApiConnectionError(RMVtransportError):
    """When a connection error is encountered."""

    pass


class RMVJourney(object):
    """A journey object to hold information about a journey."""

    def __init__(self, journey, now):
        """Initialize the journey object."""
        self.journey = journey
        self.now = now
        self.attr_types = self.journey.JourneyAttributeList.xpath(
            '*/Attribute/@type')

        self.name = self._extract('NAME')
        self.number = self._extract('NUMBER')
        self.product = self._extract('CATEGORY')
        self.trainId = self.journey.get('trainId')
        self.departure = self._departure()
        self.delay = self._delay()
        self.real_departure_time = self._real_departure_time()
        self.real_departure = self._real_departure()
        self.direction = self._extract('DIRECTION')
        self.info = self._info()
        self.info_long = self._info_long()
        self.platform = self._platform()
        self.stops = self._pass_list()
        self.icon = self._icon()

    def _platform(self):
        """Extract platform."""
        try:
            return self.journey.MainStop.BasicStop.Dep.Platform.text
        except AttributeError:
            return None

    def _delay(self):
        """Extract departure delay."""
        try:
            return int(self.journey.MainStop.BasicStop.Dep.Delay.text)
        except AttributeError:
            return 0

    def _departure(self):
        """Extract departure time."""
        departure_time = datetime.strptime(
            self.journey.MainStop.BasicStop.Dep.Time.text,
            '%H:%M').time()
        if departure_time > (self.now - timedelta(hours=1)).time():
            return datetime.combine(self.now.date(),
                                    departure_time)
        return datetime.combine(self.now.date() + timedelta(days=1),
                                departure_time)

    def _real_departure_time(self):
        """Calculate actual departure time."""
        return self.departure + timedelta(minutes=self.delay)

    def _real_departure(self):
        """Calculate actual minutes left for departure."""
        return round((self.real_departure_time - self.now).seconds / 60)

    def _extract(self, attribute):
        """Extract train information."""
        attr_data = self.journey.JourneyAttributeList.JourneyAttribute[
            self.attr_types.index(attribute)].Attribute
        attr_variants = attr_data.xpath('AttributeVariant/@type')
        data = attr_data.AttributeVariant[
            attr_variants.index('NORMAL')].Text.pyval
        return data

    def _info(self):
        """Extract journey information."""
        try:
            return html.unescape(
                self.journey.InfoTextList.InfoText.get('text'))
        except AttributeError:
            return None

    def _info_long(self):
        """Extract journey information."""
        try:
            return html.unescape(
                self.journey.InfoTextList.InfoText.get('textL')
                ).replace('<br />', '\n')
        except AttributeError:
            return None

    def _pass_list(self):
        """Extract next stops along the journey."""
        stops = []
        for stop in self.journey.PassList.BasicStop:
            index = stop.get('index')
            station = stop.Location.Station.HafasName.Text.text
            stationId = stop.Location.Station.ExternalId.text
            stops.append({'index': index,
                          'stationId': stationId,
                          'station': station})
        return stops

    def _icon(self):
        """Extract product icon."""
        pic_url = "https://www.rmv.de/auskunft/s/n/img/products/%i_pic.png"
        return pic_url % PRODUCTS[self.product]


class RMVtransport(object):
    """Connection data and travel information."""

    def __init__(self, session, timeout = 10):
        """Initialize connection data."""
        self._session = session
        self._timeout = timeout

        self.base_uri = 'http://www.rmv.de/auskunft/bin/jp/'
        self.query_path = 'query.exe/'
        self.getstop_path = 'ajax-getstop.exe/'
        self.stboard_path = 'stboard.exe/'

        self.lang = 'd'
        self.type = 'n'
        self.with_suggestions = '?'

        self.http_headers = {}

        self.now = None
        self.tz = 'CET'

        self.station = None
        self.stationId = None
        self.directionId = None
        self.productsFilter = None

        self.maxJourneys = None

        self.o = None
        self.journeys = []

    async def get_departures(self, stationId, directionId=None,
                       maxJourneys=20, products=ALL):
        """Fetch data from rmv.de."""
        self.stationId = stationId
        self.directionId = directionId

        self.maxJourneys = maxJourneys

        self.productsFilter = _product_filter(products)

        base_url = self._base_url()
        params = {'selectDate':     'today',
                  'time':           'now',
                  'input':          self.stationId,
                  'maxJourneys':    self.maxJourneys,
                  'boardType':      'dep',
                  'productsFilter': self.productsFilter,
                  'disableEquivs':  'discard_nearby',
                  'output':         'xml',
                  'start':          'yes'}
        if self.directionId:
            params['dirInput'] = self.directionId

        url = base_url + urllib.parse.urlencode(params)

        try:
            with async_timeout.timeout(self._timeout):
                response = await self._session.get(url)

            _LOGGER.debug(
                "Response from RMV API: %s", response.status)
            xml = await response.read()
            _LOGGER.debug(xml)
        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Can not load data from RMV API")
            raise RMVtransportApiConnectionError()

        try:
            self.o = objectify.fromstring(xml)
        except (TypeError, etree.XMLSyntaxError):
            _LOGGER.debug("Get from string: %s", xml[:100])
            raise RMVtransportError()

        try:
            self.now = self.current_time()
            self.station = self._station()
        except (TypeError, AttributeError):
            _LOGGER.debug("Time/Station TypeError or AttributeError",
                          objectify.dump(self.o))
            raise RMVtransportError()

        self.journeys.clear()
        try:
            for journey in self.o.SBRes.JourneyList.Journey:
                self.journeys.append(RMVJourney(journey, self.now))
        except AttributeError:
            _LOGGER.debug("Extract journeys: %s", self.o.SBRes.Err.get('text'))
            raise RMVtransportError()

        return self.to_json()

    def to_json(self):
        """Return travel data as JSON."""
        data = {}
        data['station'] = (self.station)
        data['stationId'] = (self.stationId)
        data['filter'] = (self.productsFilter)

        journeys = []
        for j in sorted(
                self.journeys,
                key=lambda k: k.real_departure)[:self.maxJourneys]:
            journeys.append({'product': j.product,
                             'number': j.number,
                             'trainId': j.trainId,
                             'direction': j.direction,
                             'departure_time': j.real_departure_time,
                             'minutes': j.real_departure,
                             'delay': j.delay,
                             'stops': [s['station'] for s in j.stops],
                             'info': j.info,
                             'info_long': j.info_long,
                             'icon': j.icon})
        data['journeys'] = (journeys)
        return data

    def _base_url(self):
        """Build base url."""
        return (self.base_uri + self.stboard_path + self.lang +
                self.type + self.with_suggestions)

    def _station(self):
        """Extract station name."""
        return self.o.SBRes.SBReq.Start.Station.HafasName.Text.pyval

    def current_time(self):
        """Extract current time."""
        if self.o is not None and self.o.SBRes.find('SBReq') is not None:
            _date = datetime.strptime(
                self.o.SBRes.SBReq.StartT.get("date"), '%Y%m%d')
            _time = datetime.strptime(
                self.o.SBRes.SBReq.StartT.get("time"), '%H:%M')
            return datetime.combine(_date.date(), _time.time())

    def output(self):
        """Pretty print travel times."""
        print("%s - %s" % (self.station, self.now))
        print(self.productsFilter)

        for j in sorted(
                self.journeys,
                key=lambda k: k.real_departure)[:self.maxJourneys]:
            print("-------------")
            print("%s: %s (%s)" % (j.product, j.number, j.trainId))
            print("Richtung: %s" % (j.direction))
            print("Abfahrt in %i min." % (j.real_departure))
            print("Abfahrt %s (+%i)" % (j.departure.time(), j.delay))
            print("Nächste Haltestellen: %s" % (
                [s['station'] for s in j.stops]))
            if j.info:
                print("Hinweis: %s" % (j.info))
                print("Hinweis (lang): %s" % (j.info_long))
            print("Icon: %s" % j.icon)


def _product_filter(products):
    """Calculate the product filter."""
    _filter = 0
    for p in set([PRODUCTS[p] for p in products]):
        _filter += p
    return format(_filter, 'b')[::-1]
