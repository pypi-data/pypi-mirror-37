"""Define endpoints related to user reports."""
from typing import Callable, Coroutine

from aiocache import cached

from .util import haversine


class UserReport:  # pylint: disable=too-few-public-methods
    """Define a single class to handle these endpoints."""

    def __init__(
            self, request: Callable[..., Coroutine], latitude: float,
            longitude: float, cache_seconds: int) -> None:
        """Initialize."""
        self._request = request
        self._latitude = latitude
        self._longitude = longitude

        self.dump = cached(ttl=cache_seconds)(self._dump)

    async def _dump(self) -> dict:
        """Dump the raw API results (cached)."""
        return await self._request('get', 'map/markers')

    async def status(self) -> dict:
        """Get symptom data for the location nearest to the user's lat/lon."""
        data = [
            d for d in await self.dump() if d['latitude'] and d['longitude']
        ]
        closest = min(
            data,
            key=lambda p: haversine(
                self._latitude,
                self._longitude,
                float(p['latitude']),
                float(p['longitude'])
            ))
        return closest

    async def status_by_zip(self, zip_code: str) -> dict:
        """Get symptom data for the location nearest to the user's lat/lon."""
        try:
            [info] = [
                d for d in await self.dump() if d['zip'] == zip_code
            ]
        except ValueError:
            return {}

        return info
