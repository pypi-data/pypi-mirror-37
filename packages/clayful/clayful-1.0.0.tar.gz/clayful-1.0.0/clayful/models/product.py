class Product:

	Clayful = None
	name = 'Product'
	path = 'products'

	@staticmethod
	def config(clayful):

		Product.Clayful = clayful

		return Product

	@staticmethod
	def list(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/products',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/products/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/products/{productId}',
			'params':           ('productId', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/{productId}/meta/{field}/inc',
			'params':           ('productId', 'field', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/{productId}/meta/{field}/push',
			'params':           ('productId', 'field', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/{productId}/meta/{field}/pull',
			'params':           ('productId', 'field', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/products/{productId}/meta/{field}',
			'params':           ('productId', 'field', ),
			'args':             args
		})

