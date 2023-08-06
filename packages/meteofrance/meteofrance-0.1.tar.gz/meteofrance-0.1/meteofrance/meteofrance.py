"""
Meteo France raining forecast.
"""

import requests
from bs4 import BeautifulSoup

RAIN_FORECAST_API = 'http://www.meteofrance.com/mf3-rpc-portlet/rest/pluie/{}/'
WEATHER_FORECAST_URL = 'http://www.meteofrance.com/previsions-meteo-france/chars/{}'

class meteofranceError(Exception):
    """Raise when errors occur while fetching or parsing MeteoFrance data"""

class meteofrance(object):
    def __init__(self, postal_code, insee_code):
        """Initialize the client object."""
        if len(str(insee_code)) == 5:  # convert insee code to needed meteofrance code
            self.insee_code = str(insee_code)+'0'
        else:
            self.insee_code = insee_code
        self.postal_code = postal_code
        self._rain_forecast = False
        self._weather_html_soup = False
        self._data = {}
        self.update()

    def update(self):
        """Fetch new data and format it"""
        self._fetch_foreacast_data()
        self._fetch_rain_forecast()
        self._format_data()

    def _fetch_rain_forecast(self):
        """Get the latest data from Meteo-France."""
        url = RAIN_FORECAST_API.format(self.insee_code)
        try:
            result = requests.get(url, timeout=10).json()
            if result['hasData'] is True:
                self._rain_forecast = result
            else:
                raise meteofranceError("This location has no rain forecast available")
        except ValueError as err:
            raise meteofranceError("Error while fetch rain forecast")
        return

    def _fetch_foreacast_data(self):
        """Get the forecast and current weather from Meteo-France."""
        url = WEATHER_FORECAST_URL.format(self.postal_code)
        try:
            result = requests.get(url, timeout=10)
            if result.status_code is 200:
                soup = BeautifulSoup(result._content, 'html.parser')
                if soup.find(class_="day-summary-label") is not None:
                    self._weather_html_soup = soup
                    return
            raise meteofranceError("Error while fetch weather forecast")
        except ValueError as err:
            raise meteofranceError("Error while fetch weather forecast")

    def _get_next_rain_time(self):
        """Get the minutes to the next rain"""
        time_to_rain = 0
        for interval in self._rain_forecast["dataCadran"]:
            if interval["niveauPluie"] > 1:
                return time_to_rain
            time_to_rain += 5
        return "No rain"

    def _format_data(self):
        """Format data from JSON and HTML returned by Meteo-France."""
        rain_forecast = self._rain_forecast
        if rain_forecast is not False:
            self._data["rain_foreacast"] = rain_forecast["niveauPluieText"][0]
            self._data["next_rain"] = self._get_next_rain_time()
            self._data["next_rain_intervals"] = {}
            for interval in range(0, len(rain_forecast["dataCadran"])):
                self._data["next_rain_intervals"]["rain_level_"+str(interval*5)+"min"] = rain_forecast["dataCadran"][interval]["niveauPluie"]
        soup = self._weather_html_soup
        if soup is not False:
            self._data["weather"] = soup.find(class_="day-summary-label").string
            self._data["temperature"] = soup.find(class_="day-summary-temperature").string
            self._data["wind_speed"] = next(soup.find(class_="day-summary-wind").stripped_strings)
            #wind_bearing
            #humidity
            day_probabilities = soup.find(class_="day-probabilities").find_all("li")
            self._data["rain_chance"] = day_probabilities[0].strong.string
            self._data["thunder_chance"] = day_probabilities[1].strong.string
            self._data["freeze_chance"] = day_probabilities[2].strong.string
            self._data["snow_chance"] = day_probabilities[3].strong.string
            #pressure
            #clouds
            #weather_code

    def get_data(self):
        """Return formatted data of current forecast"""
        return self._data
