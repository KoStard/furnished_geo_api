from collections import OrderedDict, defaultdict
import asyncio
import aiohttp
import json


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_page(
        layer,
        check_in_time,
        check_out_time,
        page,
        path=None,
        min_price=10,
        max_price=2500,
        min_mates=1,
        max_mates=30,
        room_type="All",
        district="All",
        hotel=0,
        limitAll=9,
        use_json=True,
):
    data = OrderedDict((
        ("path", path),
        ("min_price", min_price),
        ("max_price", max_price),
        ("min_mates", min_mates),
        ("max_mates", max_mates),
        ("room_type", room_type),
        ("district", district),
        ("checkintime", check_in_time),
        ("checkouttime", check_out_time),
        ("hotel", hotel),
        ("page", page),
        ("limitAll", limitAll),
    ))
    url = (f'https://www.furnished.lu/index.php?'
           f'route=module/layer_navigation/{layer}&'
           f'https://www.furnished.lu/index.php?'
           f'route=product/category&' + "&".join("{}={}".format(k, v)
                                                 for (k, v) in data.items()
                                                 if v is not None))
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        resp = await fetch(session, url)
    print(f"Loaded page {page} from {url}")
    if use_json:
        return json.loads(resp)
    else:
        return resp
