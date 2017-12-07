import googlemaps
import requests


# Class containing functions used to communicate with the Google API. This is used to provide
# the user of the smartmirror information about travel time depending on user-set parameters.
# The user can choose a destination and travel-type. The origin of the travel is always set
# according to the IP of the smartmirror.
#
# NOTE:
# The origin is bugged on the networks at school. The geo-location service returns
# Trondheim or Asker when given an IP address from the school network. This will
# naturally provide weird travelling information. 
class Travel(object):

    google_api = None
	# Using freegeoip to geolocate IP address
    freegeoip = "http://freegeoip.net/json"
    geo_request = None
    geo_json = None

    def __init__(self):
		# Provide API key to googlemaps service
        self.google_api = googlemaps.Client(key='AIzaSyBfn7FdXwhrzcDaVBPbuE00t71r7cqG36Y')
        try:
			# Get HTTP request from freegeoip
            self.geo_request = requests.get(self.freegeoip)
			# Receive the geo_request as JSON
            self.geo_json = self.geo_request.json()
        except requests.exceptions.RequestException:
            print('Could not initialize google maps API')
            self.geo_request = None

	# Function used to get the travel time depending on end destination and chosen travel-mode
    def get_travel_time(self, destination, travel_mode, language = "en"):
        if self.geo_json is not None:
            distance_matrix = self.__get_distance_matrix(destination, travel_mode, language)
            places = self.__get_destination(destination)
			# Create the response as a python dictionary for easier usage
            travel_response = {
                'origin': distance_matrix['origin_addresses'][0],
                'destination_address': distance_matrix['destination_addresses'][0],
                'destination_name': places['results'][0]['name'],
                'distance': distance_matrix['rows'][0]['elements'][0]['distance']['text'],
                'duration': distance_matrix['rows'][0]['elements'][0]['duration']['text'],
                'travel_mode': travel_mode
            }
            return travel_response
        else:
            return None

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

