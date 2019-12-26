import argparse

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Load all available results from Furnished.lu')
    parser.add_argument('check_in_time', help='YYYY-MM-DD')
    parser.add_argument('check_out_time', help='YYYY-MM-DD')
    parser.add_argument('--path', default=110, type=int)
    parser.add_argument(
        '--min_price', default=10, help="Minimum price", type=int)
    parser.add_argument(
        '--max_price', default=2500, help="Maximum price", type=int)
    parser.add_argument(
        '--min_mates', default=1, help="Minimum Roommates", type=int)
    parser.add_argument(
        '--max_mates', default=30, help="Maxmimum Roommates", type=int)
    parser.add_argument('--room_type', default="All", help="Room type")
    parser.add_argument('--district', default="All", help="District")
    parser.add_argument('--hotel', default=0)
    return parser
