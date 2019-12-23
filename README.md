# furnished_geo_api
API to get GEO data of rooms from Furnisher.lu
This tool is created for using from the command line:
```shell
$ python3 furnished_geo_api.py 2020-01-15 2020-03-31 --path=110 --min_price=10 \
    --max_price=2500 \--min_mates=1 --max_mates=30 --room_type=All \
        --district=All --hotel=0
```

You will just get the output as a JSON text.

Or just this (same result)
```shell
$ python3 furnished_geo_api.py 2020-01-15 2020-03-31
```

You can use `to_gmaps` to get HTML document with all these points on the Google Maps:
```shell
$ python3 furnished_geo_api.py 2020-01-15 2020-03-31 --to_gmaps
```
