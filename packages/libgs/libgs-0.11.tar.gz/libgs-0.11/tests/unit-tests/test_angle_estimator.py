import sys, os
from os.path import dirname

_adfags_path = dirname(dirname(dirname(os.path.realpath(__file__)))) + '/src/adfagslib/' 
sys.path.insert(0, _adfags_path)

from  adfags import Propagator, Defaults

import requests
import json
from math import pi
import datetime
import pytest
import pandas as pd
import numpy as np
import ephem

@pytest.fixture
def propagator():
       
    # AngleEstimator needs a space-track login
    req = requests.get("https://www.celestrak.com/NORAD/elements/stations.txt")
    tles =  req.content
    tles = tles.replace('\r','').split('\n')
    tles[::3] = ['0 '+s for s in tles[::3]]
    tles='\n'.join(tles)
    return Propagator(tles=tles)


@pytest.fixture
def time_array():
    t = ephem.Date(pd.Timestamp.utcnow())
    x = np.linspace(t, t+1, 1000)
    return x



def test_get_all(propagator, time_array):
    p = propagator
    t = time_array
    
    d = p.get_all(25544, when=t)
    
    assert(len(d) == len(t))
    
    return d
        

def test_ground_track(propagator):
    """
    Unit test for AngleEstimator class.
    
    Will calculate the ground track lat/long and compare  against online source
    """
    

    # get position for the ISS
    a = propagator
    
    

    
    #
    # As an independent reference, this script is using
    # http://open-notify.org/Open-Notify-API/ISS-Location-Now/ which
    # has a simple json API that scrapes NASA.
    #
    req = requests.get("http://api.open-notify.org/iss-now.json")
    obj = json.loads(req.content)
    
    reflat = float(obj['iss_position']['latitude'])
    reflon = float(obj['iss_position']['longitude'])
    refdate = datetime.datetime.utcfromtimestamp(obj["timestamp"]).strftime('%Y/%m/%d %H:%M:%S')
    

    lat,lon = a.get_ground_coord(25544, when=refdate)
    
    print("Using timestamp (UTC): %s"%(refdate))
    print("%5s%15s%15s"%("","ADFAGS", "iss-now"))
    print("%5s%15f%15f"%("lat", lat, reflat ))
    print("%5s%15f%15f"%("lon", lon, reflon ))

    assert abs(lat - reflat) < 0.3, "Ground track latitude estimate not matching iss-now"
    assert abs(lon - reflon) < 0.3, "Ground track longitude estimate not matching iss-now"
    
    

if __name__ == '__main__':
    p = propagator()
    test_ground_track(p)

