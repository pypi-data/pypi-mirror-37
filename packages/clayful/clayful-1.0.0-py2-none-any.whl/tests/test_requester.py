import unittest
import httpretty
from clayful.exception import ClayfulException
from clayful.requester import request

class ClayfulRequesterTest(unittest.TestCase):

	@httpretty.activate
	def test_request_with_query_and_headers(self):

		httpretty.register_uri(
			httpretty.GET,
			'https://api.clayful.io/v1/products',
			body='{ "success": true }',
			status=200,
			content_type='application/json'
		)

		result = request({
			'model_name':    'Product',
			'method_name':   'query',
			'http_method':   'GET',
			'request_url':   'https://api.clayful.io/v1/products',
			'query':         { 'raw': 'true' },
			'headers':       {
				'Authorization': 'Bearer client_token'
			},
			'payload':        None,
			'uses_form_data': False
		})

		last_request = httpretty.last_request()

		# Check query, headers
		self.assertEqual(last_request.path, '/v1/products?raw=true')
		self.assertEqual(last_request.headers.dict['authorization'], 'Bearer client_token')

		# Check the response
		self.assertEqual(result.status, 200)
		self.assertEqual(result.data['success'], True)
		self.assertEqual(result.headers['Content-Type'], 'application/json')


	@httpretty.activate
	def test_request_with_json_payload(self):

		httpretty.register_uri(
			httpretty.POST,
			'https://api.clayful.io/v1/products',
			body='{ "success": true }',
			status=201
		)

		result = request({
			'model_name':    'Product',
			'method_name':   'create',
			'http_method':   'POST',
			'request_url':   'https://api.clayful.io/v1/products',
			'query':         {},
			'headers':       {
				'Authorization': 'Bearer client_token'
			},
			'payload':        { 'name': {} },
			'uses_form_data': False
		})

		last_request = httpretty.last_request()

		# Check headers
		self.assertEqual(last_request.headers.dict['content-type'], 'application/json')

		self.assertEqual(result.status, 201)


	@httpretty.activate
	def test_request_with_multipart_form_data(self):

		httpretty.register_uri(
			httpretty.POST,
			'https://api.clayful.io/v1/images',
			body='{ "success": true }',
			status=201
		)

		result = request({
			'model_name':    'Image',
			'method_name':   'create',
			'http_method':   'POST',
			'request_url':   'https://api.clayful.io/v1/images',
			'query':         {},
			'headers':       {
				'Authorization': 'Bearer client_token'
			},
			'payload':        { 'file': 'file' },
			'uses_form_data': True
		})

		last_request = httpretty.last_request()

		# Check headers
		self.assertTrue('multipart/form-data' in last_request.headers.dict['content-type'])

		self.assertEqual(result.status, 201)


	@httpretty.activate
	def test_empty_response(self):

		httpretty.register_uri(
			httpretty.DELETE,
			'https://api.clayful.io/v1/products/abcdefg',
			status=204
		)

		result = request({
			'model_name':    'Product',
			'method_name':   'delete',
			'http_method':   'DELETE',
			'request_url':   'https://api.clayful.io/v1/products/abcdefg',
			'query':         {},
			'headers':       {
				'Authorization': 'Bearer client_token'
			},
			'payload':        None,
			'uses_form_data': False
		})

		self.assertEqual(result.status, 204)
		self.assertEqual(result.data, None)


	@httpretty.activate
	def test_clayful_error_case(self):

		httpretty.register_uri(
			httpretty.GET,
			'https://api.clayful.io/v1/products',
			body='{ "errorCode": "g-validation", "message": "validation error", "validation": {  } }',
			status=400,
			content_type='application/json'
		)

		try:

			request({
				'model_name':    'Product',
				'method_name':   'query',
				'http_method':   'GET',
				'request_url':   'https://api.clayful.io/v1/products',
				'query':         {},
				'headers':       {
					'Authorization': 'Bearer client_token'
				},
				'payload':        None,
				'uses_form_data': False
			})

		except ClayfulException as e:

			self.assertEqual(e.is_clayful, True)
			self.assertEqual(e.model, 'Product')
			self.assertEqual(e.method, 'query')
			self.assertEqual(e.status, 400)
			self.assertEqual(e.headers['Content-Type'], 'application/json')
			self.assertEqual(e.code, 'g-validation')
			self.assertEqual(e.message, 'validation error')
			self.assertEqual(e.validation, {})