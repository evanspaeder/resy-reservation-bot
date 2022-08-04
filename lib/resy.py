from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import certifi
from datetime import datetime
import json

cafile = certifi.where()

def request(api_key, auth_token, url, params = {}, method = "GET", content_type = "application/json"):
    headers = {
        "Authorization": 'ResyAPI api_key="' + api_key +'"',
        "x-resy-auth-token": auth_token
    }
    if method == "GET":
        url = url + "?" + urlencode(params)
        data = None
    elif content_type == "application/json":
        data = json.dumps(params).encode('utf-8')
        headers.update({
            "content-type": content_type
        })
    elif content_type == "application/x-www-form-urlencoded":
        data = urlencode(params).encode('utf-8')
        headers.update({
            "content-type": content_type
        })

    response = urlopen(Request(url, data=data, headers=headers, method=method), cafile=cafile).read().decode('utf-8')

    return json.loads(response)

class Resy:

    def __init__(self, api_key, auth_token):
        self.api_key = api_key
        self.auth_token = auth_token

        print("Sending test request to validate resy keys")
        try:
            request(
                api_key= self.api_key,
                auth_token= self.auth_token,
                url = "https://api.resy.com/2/user"
            )
            print("Your Resy keys are working")
        except HTTPError as err:
            if err.code == 419:
                print("Your Resy API keys are wrong")
            else:
                print("IDK what happened")


    def findReservations(self, day, party_size, venue_id):
        params = {
            "lat": "0",
            "long": "0",
            "day": day.strftime("%Y-%m-%d"),
            "party_size": str(party_size),
            "venue_id": str(venue_id)
        }
        reservations = request(
            api_key= self.api_key,
            auth_token= self.auth_token,
            url = "https://api.resy.com/4/find",
            params= params
        )
        return reservations['results']['venues'][0]['slots']
        
    def getReservationDetails(self, config_id, day, party_size):
        params = {
            "config_id": config_id,
            "day": day.strftime("%Y-%m-%d"),
            "party_size": party_size
        }
        details = request(
            api_key= self.api_key,
            auth_token= self.auth_token,
            url = "https://api.resy.com/3/details",
            params= params,
            method="POST"
        )
        return details

    def bookReservation(self, book_token, payment_method_id):
        params = {
            "book_token": book_token,
            "struct_payment_method": '{"id":' + str(payment_method_id) + '}',
            "source_id": "resy.com-venue-details"
        }
        booking = request(
            api_key= self.api_key,
            auth_token= self.auth_token,
            url = "https://api.resy.com/3/book",
            params= params,
            method="POST",
            content_type= "application/x-www-form-urlencoded"
        )
        return booking
    