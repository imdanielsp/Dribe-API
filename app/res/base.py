from flask import Response

JSON_TYPE = 'application/json'
NOT_FOUND_MSG = '{"message": "The requested record was not found.", "status": "ERROR"}'
OK_MSG = '{"message": "OK"}'
GENERIC_MSG = '{"message": "%s"}'
DRIVER_ONLINE = '{"status": "ONLINE", "lat": %f, "lng": %f}'
DRIVER_OFFLINE = '{"status": "OFFLINE"}'


def get_not_found_response():
	return Response(NOT_FOUND_MSG, status=404, mimetype=JSON_TYPE)
