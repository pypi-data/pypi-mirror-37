import requests
import base64
import json


class Vasttrafik(object):

    def __init__(self, key, secret, device='test'):
        self.key = key
        self.secret = secret
        self.device = device
        self.base_url = 'https://api.vasttrafik.se/bin/rest.exe/v2'
        self.token = self.get_token()

    def get_token(self):
        return json.loads(requests.post(
            'https://api.vasttrafik.se/token',
            headers={
                'Authorization': 'Basic {}'.
                format(base64.b64encode('{}:{}'.format(self.key, self.secret)))
            },
            data={
                'grant_type': 'client_credentials',
                'scope': 'device_'.format(self.device)
            }
        ).text)['access_token']

    def get_headers(self):
        return {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'api.vasttrafik.se',
            'Origin': 'https://developer.vasttrafik.se',
            'Pragma': 'no-cache',
            'Referer': 'https://developer.vasttrafik.se/portal/'
        }

    def _get(self, endpoint, data):
        return requests.get(
            self.base_url + endpoint + '?format=json&' + '&'.
            join('{}={}'.format(k, v) for k, v in data.items()),
            headers=self.get_headers()
        )

    def api_location_name(self, name):
        return json.loads(self._get(
            '/location.name', dict(input=name)).text
        )['LocationList']['StopLocation']

    def api_trip(self, origin_id, destination_id):
        return json.loads(self._get(
            '/trip', dict(originId=origin_id, destId=destination_id)).text)

    def api_departure_board(self, origin_id):
        return json.loads(self._get(
            '/departureBoard', dict(id=origin_id)).text)['DepartureBoard']

    def api_arrival_board(self, origin_id):
        return json.loads(self._get(
            '/arrivalBoard', dict(id=origin_id)).text)['ArrivalBoard']
