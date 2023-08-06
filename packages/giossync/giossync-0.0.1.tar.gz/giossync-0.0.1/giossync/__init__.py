"""asyncio-friendly python API for gios (http://powietrze.gios.gov.pl)."""
import asyncio
import aiohttp
import async_timeout

BASE_URL = 'http://api.gios.gov.pl/pjp-api/rest/'
SENSORS_URL = BASE_URL + 'station/sensors/{}/'
SENSOR_DATA_URL = BASE_URL + 'data/getData/{}/'


class GiosClient(object):
    """Gios client implementation."""

    def __init__(self, station, session=None, timeout=aiohttp.client.DEFAULT_TIMEOUT):
        """Constructor.
        
        station: Station Id from http://powietrze.gios.gov.pl/pjp/current#
        session: aiohttp.ClientSession or None to create a new session.
        """
        self._station = station
        self._timeout = timeout
        if session is not None:
            self._session = session
        else:
            self._session = aiohttp.ClientSession()

    @asyncio.coroutine
    def get_sensor_by_station_id(self, station_id):
        """Get sensors by station_id."""
        return (yield from self._get(SENSORS_URL.format(station_id)))

    @asyncio.coroutine
    def get_sensor_data(self, sensor_id):
        """Get sensor data by sensor_id."""
        return (yield from self._get(SENSOR_DATA_URL.format(sensor_id)))

    @asyncio.coroutine
    def _get(self, path, **kwargs):
        with async_timeout.timeout(self._timeout):
            resp = yield from self._session.get(
                path, params=dict(self._params, **kwargs))
            return (yield from resp.json())['data']
