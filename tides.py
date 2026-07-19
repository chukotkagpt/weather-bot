import os
import httpx

LAT = 69.7008
LON = 170.3133

TIDES_API_KEY = os.environ["TIDES_API_KEY"]


async def get_tides():

    url = (
        "https://tidesatlas.com/api/v1/tides"
        f"?lat={LAT}"
        f"&lon={LON}"
        "&days=1"
    )

    headers = {
        "X-API-Key": TIDES_API_KEY
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()

    data = response.json()

    extremes = data.get("extremes", [])

    high = None
    low = None

    for tide in extremes:

        if tide["type"] == "high" and high is None:
            high = tide["datetime"][11:16]

        elif tide["type"] == "low" and low is None:
            low = tide["datetime"][11:16]

    return {
        "high": high,
        "low": low,
        "state": None
    }
