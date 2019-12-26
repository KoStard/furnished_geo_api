"""
https://www.furnished.lu/index.php?
    route=module/layer_navigation/loadData&
https://www.furnished.lu/index.php?
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
        page=1
"""

from furnished_layer_loader import get_page
from furnished_cli_parser import get_parser
from bs4 import BeautifulSoup
from bs4.element import Tag
import math
import asyncio


def get_args() -> dict:
    parser = get_parser()
    args: dict = dict(vars(parser.parse_args()))
    return args


def parse_products(products_container: Tag):
    results = {}  # id:
    products = products_container.findAll(
        'div', attrs={'class': 'product-layout'})
    for product in products:
        pr_id = product.get('data-product')
        # Product URL
        # https://www.furnished.lu/index.php?route=product/product&amp;product_id=...
        name = product.find(
            'h4', attrs={
                'class': 'single-product-name'
            }).text.strip()
        info = product.find(
            'span', attrs={
                'class': 'single-product-information'
            }).text.strip()
        price = product.find(
            'h4', attrs={
                'class': 'single-product-price'
            }).text.strip()
        results[pr_id] = {'info': info, 'price': price, 'name': name}
    return results


async def get_pricing(**kwargs):
    raw_html = await get_page(
        **kwargs, use_json=False, layer="loadData", page=1)
    dom = BeautifulSoup(raw_html, features="lxml")
    rows = dom.findAll('div', attrs={'class': 'row'})
    results = {}
    if not rows:
        return results
    products_container, counts = rows

    results.update(parse_products(products_container))

    per_page = int(counts.find('span', attrs={'class': 'max-results'}).text)
    total_count = int(
        counts.find('span', attrs={
            'class': 'total-filtered'
        }).text)

    for page in range(2, math.ceil(total_count / per_page) + 1):
        raw_html = await get_page(
            **kwargs, use_json=False, layer="loadData", page=page)
        dom = BeautifulSoup(raw_html, features="lxml")
        rows = dom.findAll('div', attrs={'class': 'row'})
        products_container, counts = rows
        results.update(parse_products(products_container))

    return results


if __name__ == '__main__':
    args = get_args()
    print(asyncio.run(get_pricing(**args)))
