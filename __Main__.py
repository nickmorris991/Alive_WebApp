# this program queries the yelp fusion api in order to
# display & suggest restaurants and experiences to the user

# API imports
from __future__ import print_function
import urllib
import pprint
import requests
import json
import argparse
import sys


# flask imports
from flask import Flask, render_template, redirect, url_for
from wtforms import StringField, validators
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired


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


# API constants
CLIENT_ID = 'xcSzTOxuxVQRd1cKKJxaqQ'
CLIENT_SECRET = 'xQU0xYaI3T8BdsuwZdVgWCzRq19XhaDuE81uWuZwvFZBtT8QH2NR3sgvTjHTKJAR'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'
SEARCH_LIMIT = 10



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



def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()



def search(bearer_token, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'



class SearchForm(FlaskForm):
    """define two forms for user input along with validators
    to ensure input to the search query.These wil be called in
    homepage and rendered to index.html"""
    Zipcode = StringField('Enter Location:', validators=[InputRequired()])
    Keyword = StringField('Search Keywords:', validators=[InputRequired()])



@app.route('/', methods=['GET', 'POST'])
def homepage():
    """homepage of the web app asks the user to input
    their location and keywords for the search"""
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('.queryResults'))
    return render_template('index.html', form=form)



@app.route('/Results', methods=['GET', 'POST'])
def queryResults():
    """redirects user to route '/Results' to display search query
    and make suggestions on what the user should eat or do"""
    form = SearchForm()
    if form.validate_on_submit() and form.Keyword.data != '' and form.Zipcode.data !='':
        access_token = obtain_bearer_token(API_HOST, TOKEN_PATH)
        data = search(access_token, form.Keyword.data, form.Zipcode.data)
        return render_template('results.html', data=data)
    return redirect(url_for ('.homepage'))



# start the server
if __name__ == "__main__":
    app.run()
