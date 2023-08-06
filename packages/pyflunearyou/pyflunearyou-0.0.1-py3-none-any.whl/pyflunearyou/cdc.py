"""Define endpoints related to CDC reports."""
# pylint: disable=unused-import
from copy import deepcopy
from typing import Callable, Coroutine, Dict  # noqa

from aiocache import cached

STATUS_MAP = {
    1: 'No Data',
    2: 'Minimal',
    3: 'Low',
    4: 'Moderate',
    5: 'High',
    99: 'None',
}


def adjust_status(info: dict) -> dict:
    """Apply status mapping to a raw API result."""
    modified_info = deepcopy(info)
    modified_info.update({
        'level':
            STATUS_MAP[int(info['level'])],
        'level2':
            STATUS_MAP[int(99 if info['level2'] is None else info['level2'])],
    })

    return modified_info


class CdcReport:  # pylint: disable=too-few-public-methods
    """Define a single class to handle these endpoints."""

    def __init__(
            self, request: Callable[..., Coroutine], contained_by_id: str,
            cache_seconds: int) -> None:
        """Initialize."""
        self._contained_by_id = contained_by_id
        self._request = request

        self.dump = cached(ttl=cache_seconds)(self._dump)

    async def _dump(self) -> dict:
        """Dump the raw API results (cached)."""
        return await self._request('get', 'map/cdc')

    async def status(self) -> dict:
        """Return the CDC status for the provided latitude/longitude."""
        info = {}  # type: Dict[str, str]

        data = await self.dump()
        keys = list(data.keys())
        for idx, key in enumerate(data.keys()):
            if key == self._contained_by_id:
                info = data[keys[idx + 1]]

        return info

    async def status_by_state(self, state: str) -> dict:
        """Return the CDC status for the specified state."""
        data = await self.dump()
        [info] = [v for k, v in data.items() if state in k]
        return adjust_status(info)
