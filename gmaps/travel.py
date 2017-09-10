import googlemaps
import requests


class Travel(object):

    google_api = None
    freegeoip = "http://freegeoip.net/json"
    geo_request = None
    geo_json = None

    def __init__(self):
        self.google_api = googlemaps.Client(key='AIzaSyBfn7FdXwhrzcDaVBPbuE00t71r7cqG36Y')
        self.geo_request = requests.get(self.freegeoip)
        self.geo_json = self.geo_request.json()

    def get_travel_time(self, destination, travel_mode, language):
        distance_matrix = self.__get_distance_matrix(destination, travel_mode, language)
        places = self.__get_destination(destination)

        travel_response = {
            'origin': distance_matrix['origin_addresses'][0],
            'destination_address': distance_matrix['destination_addresses'][0],
            'destination_name': places['results'][0]['name'],
            'distance': distance_matrix['rows'][0]['elements'][0]['distance']['text'],
            'duration': distance_matrix['rows'][0]['elements'][0]['duration']['text'],
            'travel_mode': travel_mode
        }

        return travel_response

    # Internal use
    def __get_destination(self, destination):
        places = self.google_api.places(destination)

        return places

    # Internal use
    def __get_distance_matrix(self, destination, travel_mode, language):
        distance_matrix = self.google_api.distance_matrix((self.geo_json['latitude'], self.geo_json['longitude']),
                                                          destination,
                                                          mode=travel_mode,
                                                          avoid=None,
                                                          language=language)

        return distance_matrix



