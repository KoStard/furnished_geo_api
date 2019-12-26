from opencage.geocoder import OpenCageGeocode
import os
key = os.environ['OPENCAGEDATA_KEY']


def get_county(lat, lng):
    # Allow running with multiple pairs to run them in parallel (at least to try)
    cgc = OpenCageGeocode(key)
    resp = cgc.reverse_geocode(lat, lng, no_annotations=1)
    return resp[0]['components']['county']
