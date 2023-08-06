import requests
from clayful.response import ClayfulResponse
from clayful.exception import ClayfulException

def request(request_options):

	options = {
		'params':  request_options.get('query', {}),
		'headers': request_options.get('headers', {}),
	}

	if request_options.get('payload') != None:

		if request_options.get('uses_form_data') == True:

			options['files'] = request_options['payload'] # multipart/form-data

		else:

			options['json'] = request_options['payload']  # application/json

	result = requests.request(
		request_options['http_method'],
		request_options['request_url'],
		**options
	)

	data = None

	try:
		data = result.json()

	except ValueError:
		data = None

	if result.status_code >= 400:

		raise ClayfulException(
			request_options.get('model_name'),
			request_options.get('method_name'),
			result.status_code,
			result.headers,
			data.get('errorCode', None),
			data.get('message', None),
			data.get('validation', None)
		)

	else:

		return ClayfulResponse(result.status_code, data, result.headers)
