import requests

import config


class MatrixApi:
    MATRIX_API_URL = ("https://maps.googleapis.com/maps/api/distancematrix/"
                      "json?units=imperial&origins={origin_latitude},{origin_longitude}"
                      "&destinations={dest_latitude},{dest_longitude}&key={API_KEY}")

    def __init__(self, request=None, origin=None, destination=None):
        if request:
            self.origin_latitude = request.origin_latitude
            self.origin_longitude = request.origin_longitude
            self.destination_latitude = request.destination_latitude
            self.destination_longitude = request.destination_longitude
        else:
            self.origin = origin
            self.destination = destination

    def get_matrix_info(self):
        url = self.get_url()
        http_response = requests.get(url)
        json_response = http_response.json()
        elements = json_response["rows"][0]["elements"][0]
        if elements["status"] == "OK":
            distance_value = elements["distance"]["value"]
            duration_value = elements["duration"]["value"]
            return distance_value, duration_value
        else:
            msg = "Matrix status is \"%s\"" % elements["status"]
            raise MatrixApi.MatrixApiError(msg)

    def get_url(self):
        if requests:
            return MatrixApi.MATRIX_API_URL.format(
                origin_latitude=self.origin_latitude,
                origin_longitude=self.origin_longitude,
                dest_latitude=self.destination_latitude,
                dest_longitude=self.destination_longitude,
                API_KEY=config.GOOGLE_API_KEY
            )
        else:
            return MatrixApi.MATRIX_API_URL.format(
                origin_latitude=self.origin[0],
                origin_longitude=self.origin[1],
                dest_latitude=self.destination[0],
                dest_longitude=self.destination[1],
                API_KEY=config.GOOGLE_API_KEY
            )

    class MatrixApiError(Exception):
        pass
