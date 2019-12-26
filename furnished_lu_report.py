from furnished_cli_parser import get_parser
from furnished_geo_api import get_locations
from furnished_pricing_api import get_pricing
import asyncio


def get_args() -> dict:
    parser = get_parser()
    args: dict = dict(vars(parser.parse_args()))
    return args


async def process(**kwargs):
    loop = asyncio.get_event_loop()

    async def run(f):
        return await f(**kwargs)

    locations_task = await loop.run_in_executor(None, run, get_locations)
    pricings_task = await loop.run_in_executor(None, run, get_pricing)

    locations = await locations_task
    pricings = await pricings_task

    print(locations, pricings)

    # Merge locations, pricings and load county names


loop = asyncio.get_event_loop()
loop.run_until_complete(process(**get_args()))
