'''

Mostly copied from Harper Reed at https://github.com/harperreed/life360-python

'''

import requests
import json
import numpy as np
try:
    from info.keys import *
except ImportError:
    print( "Cannot import from info.keys! \nPlease ensure that you have created and configured the info/keys.py module if you would like to use the locator." )
    
authorization_token = "cFJFcXVnYWJSZXRyZTRFc3RldGhlcnVmcmVQdW1hbUV4dWNyRUh1YzptM2ZydXBSZXRSZXN3ZXJFQ2hBUHJFOTZxYWtFZHI0Vg=="

Rekm = 6371     # Earth radius in km
Remi = 3958	# Earth radius in mi

def dist(lat1, lon1, lat2, lon2):
    # Euclidean distance along Earth surface in km
    ## Will add Imperial capabilities
    d = np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)
    return (d/360.) * 2 * np.pi * Rekm

class life360:
    
    base_url = "https://api.life360.com/v3/"
    token_url = "oauth2/token.json"
    circles_url = "circles.json"
    circle_url = "circles/"

    def __init__(self):
        self.authorization_token = authorization_token
        self.username = username
        self.password = password

    def make_request(self, url, params=None, method='GET', authheader=None):
        headers = {'Accept': 'application/json'}
        if authheader:
            headers.update({'Authorization': authheader, 'cache-control': "no-cache",})
        
        if method == 'GET':
            r = requests.get(url, headers=headers)
        elif method == 'POST':
            r = requests.post(url, data=params, headers=headers)

        return r.json()

    def authenticate(self):

        url = self.base_url + self.token_url
        params = {
            "grant_type":"password",
            "username":self.username,
            "password":self.password,
        }

        r = self.make_request(url=url, params=params, method='POST', authheader="Basic " + self.authorization_token)
        try:
            self.access_token = r['access_token']
            return True
        except:
            return False

    def get_circles(self):
        url = self.base_url + self.circles_url
        authheader="bearer " + self.access_token
        r = self.make_request(url=url, method='GET', authheader=authheader)
        return r['circles']

    def get_circle(self, circle_id):
        url = self.base_url + self.circle_url + circle_id
        authheader="bearer " + self.access_token
        r = self.make_request(url=url, method='GET', authheader=authheader)
        return r
        
    def get_min_dist(self):
        ''' Returns distance in kilometers of nearest member '''
        mindist = 1e3
        circles = self.get_circles()
        id = circles[0]['id']
        circle = self.get_circle(id)
        for m in circle['members']:
            try:
                lat = m['location']['latitude']
                lon = m['location']['longitude']
                mindist = min( mindist, dist( home[0], home[1], float(lat), float(lon) ) )
            except:
                pass
        return mindist


if __name__ == "__main__":
    api = life360()
    if api.authenticate():
        print( api.get_min_dist() )
