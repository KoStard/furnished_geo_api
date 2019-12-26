"""
Example URL:
https://www.furnished.lu/index.php?
    route=module/layer_navigation/getMapClusters&
hcheck_in_timefurnished.lu/index.php?
    route=product/category&
        path=110&
        min_price=10&
        max_price=2500&
        min_mates=1&
        max_mates=30&
        room_type=All&
        district=All&
        checkintime=2020-01-15&
        checkouttime=2020-03-31&
        hotel=0&
        page=1&
        limitAll=9

You can use this to load data from all pages:
python3 furnished_geo_api.py 2020-01-15 2020-03-31 --path=110 --min_price=10 \
    --max_price=2500 \--min_mates=1 --max_mates=30 --room_type=All \
        --district=All --hotel=0
"""

from collections import defaultdict
import json
import gmplot
from functools import reduce
from furnished_layer_loader import get_page
from furnished_cli_parser import get_parser
import asyncio


def get_args() -> dict:
    parser = get_parser()

    parser.add_argument(
        '--gmaps_api_key',
        help=
        ("API Key of Google Maps API, used if you want to export to a "
         "valid Google Maps file. You can get it for free from "
         "https://developers.google.com/maps/documentation/javascript/get-api-key"
         ))

    parser.add_argument(
        '--to_json',
        action='store_true',
        help='Will return the results as JSON string')
    parser.add_argument(
        '--to_gmaps',
        action='store_true',
        help='Will export the results into the Google Maps')

    args: dict = dict(vars(parser.parse_args()))
    return args


async def get_locations(
        check_in_time,
        check_out_time,
        path=None,
        min_price=10,
        max_price=2500,
        min_mates=1,
        max_mates=30,
        room_type="All",
        district="All",
        hotel=0,
):
    """
    YYYY-MM-DD
    """
    page = 1
    page_data = None
    points = defaultdict(list)
    while page == 1 or page_data:
        page_data = await get_page(
            'getMapClusters',
            check_in_time,
            check_out_time,
            page,
            path,
            min_price,
            max_price,
            min_mates,
            max_mates,
            room_type,
            district,
            hotel,
        )
        for k in page_data:
            points[k].extend(page_data[k])
        page += 1

    return points


def save_to_google_maps(points: dict, filename: str, gmaps_api_key):
    points = {
        tuple(float(e) for e in k.split('/')): v
        for (k, v) in points.items()
    }
    center_x, center_y = reduce(lambda a, b: [a[0] + b[0], a[1] + b[1]],
                                points, [0, 0])
    center_x /= len(points)
    center_y /= len(points)
    plotter = gmplot.GoogleMapPlotter(
        center_x, center_y, 13, apikey=gmaps_api_key)
    for lat, lng in points:
        plotter.marker(lat, lng)

    plotter.draw(filename)


if __name__ == '__main__':
    args = get_args()
    to_json = args.pop('to_json')
    to_gmaps = args.pop('to_gmaps')
    gmaps_api_key = args.pop('gmaps_api_key')
    file_name_base = 'Options-{}-{}.'.format(args['check_in_time'],
                                             args['check_out_time'])

    points = asyncio.run(get_locations(**args))

    if to_gmaps:
        save_to_google_maps(
            points, file_name_base + 'html', gmaps_api_key=gmaps_api_key)

    if to_json or not to_gmaps:
        print(json.dumps(points))
