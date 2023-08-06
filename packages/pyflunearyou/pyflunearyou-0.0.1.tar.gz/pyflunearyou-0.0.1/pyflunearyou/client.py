"""Define a client to interact with Flu Near You."""
# pylint: disable=unused-import
from typing import Union  # noqa

from aiohttp import ClientSession, client_exceptions

from .cdc import CdcReport
from .const import DEFAULT_CACHE_SECONDS
from .errors import RequestError
from .user import UserReport

API_URL_SCAFFOLD = 'https://api.v2.flunearyou.org'

DEFAULT_HOST = 'api.v2.flunearyou.org'
DEFAULT_ORIGIN = 'https://flunearyou.org'
DEFAULT_REFERER = 'https://flunearyou.org/'
DEFAULT_USER_AGENT = 'Home Assistant (Macintosh; OS X/10.14.0) GCDHTTPRequest'


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class Client:
    """Define the client."""

    def __init__(
            self,
            latitude: float,
            longitude: float,
            websession: ClientSession,
            *,
            cache_seconds: int = DEFAULT_CACHE_SECONDS) -> None:
        """Initialize."""
        self._cache_seconds = cache_seconds
        self._latitude = latitude
        self._longitude = longitude
        self._websession = websession
        self.cdc_reports = None  # type: Union[None, CdcReport]
        self.city = None  # type: Union[None, str]
        self.user_reports = None  # type: Union[None, UserReport]
        self.zip_code = None  # type: Union[None, str]

    async def initialize(self) -> None:
        """Run some port-dunder initialization."""
        # Initialize the user_reports endpoint:
        self.user_reports = UserReport(
            self._request, self._latitude, self._longitude,
            self._cache_seconds)
        user_data = await self.user_reports.status()

        # Initialize the cdc_reports endpoint:
        self.cdc_reports = CdcReport(
            self._request, user_data['contained_by'], self._cache_seconds)

        # Set some useful properties:
        self.city = user_data['city'].split('(')[0]
        self.zip_code = user_data['zip']

    async def _request(
            self, method: str, endpoint: str, *, headers: dict = None) -> dict:
        """Make a request against air-matters.com."""
        url = '{0}/{1}'.format(API_URL_SCAFFOLD, endpoint)

        if not headers:
            headers = {}
        headers.update({
            'Host': DEFAULT_HOST,
            'Origin': DEFAULT_ORIGIN,
            'Referer': DEFAULT_REFERER,
            'User-Agent': DEFAULT_USER_AGENT,
        })

        async with self._websession.request(
                method,
                url,
                headers=headers,
        ) as resp:
            try:
                resp.raise_for_status()
                return await resp.json(content_type=None)
            except client_exceptions.ClientError as err:
                raise RequestError(
                    'Error requesting data from {0}: {1}'.format(
                        endpoint, err)) from None


async def create_client(
        latitude: float, longitude: float,
        websession: ClientSession) -> Client:
    """Create a client."""
    client = Client(latitude, longitude, websession)
    await client.initialize()
    return client
