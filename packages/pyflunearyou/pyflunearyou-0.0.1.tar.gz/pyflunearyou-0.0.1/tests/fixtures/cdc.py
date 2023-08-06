"""Define fixtures for the CDC reports endpoint."""
import pytest


@pytest.fixture()
def fixture_cdc_report_json():
    """Return a subset of a /map/cdc response."""
    return {
        "204": {
            "place_id": "204"
        },
        "California": {
            "level": "3",
            "level2": None,
            "week_date": "2018-10-13",
            "name": "California",
            "fill": {
                "color": "#00B7B6",
                "opacity": 0.7
            }
        },
        "209": {
            "place_id": "209"
        },
        "Colorado": {
            "level": "2",
            "level2": None,
            "week_date": "2018-10-13",
            "name": "Colorado",
            "fill": {
                "color": "#00B7B6",
                "opacity": 0.7
            }
        }
    }
