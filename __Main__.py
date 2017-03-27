# this program queries the yelp fusion api in order to
# display & suggest restaurants and experiences to the user

# code imports
from __future__ import print_function
import urllib
import pprint
import requests
import json
import argparse
import sys
from flask import Flask, render_template


try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode

except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode
CLIENT_ID = 'xcSzTOxuxVQRd1cKKJxaqQ'
CLIENT_SECRET = 'xQU0xYaI3T8BdsuwZdVgWCzRq19XhaDuE81uWuZwvFZBtT8QH2NR3sgvTjHTKJAR'

# API constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# a POST call to obtain access token
def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID
    assert CLIENT_SECRET
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token


#main function for homepage
app = Flask(__name__)

@app.route('/')

def homepage():
    return render_template("index.html")
print

if __name__ == "__main__":
    app.run()
