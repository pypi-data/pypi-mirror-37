class Brand:

	Clayful = None
	name = 'Brand'
	path = 'brands'

	@staticmethod
	def config(clayful):

		Brand.Clayful = clayful

		return Brand

	@staticmethod
	def list(*args):

		return Brand.Clayful.call_api({
			'model_name':       Brand.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/brands',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Brand.Clayful.call_api({
			'model_name':       Brand.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/brands/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Brand.Clayful.call_api({
			'model_name':       Brand.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/brands/{brandId}',
			'params':           ('brandId', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Brand.Clayful.call_api({
			'model_name':       Brand.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/brands/{brandId}/meta/{field}/pull',
			'params':           ('brandId', 'field', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Brand.Clayful.call_api({
			'model_name':       Brand.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/brands/{brandId}/meta/{field}/push',
			'params':           ('brandId', 'field', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Brand.Clayful.call_api({
			'model_name':       Brand.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/brands/{brandId}/meta/{field}/inc',
			'params':           ('brandId', 'field', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Brand.Clayful.call_api({
			'model_name':       Brand.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/brands/{brandId}/meta/{field}',
			'params':           ('brandId', 'field', ),
			'args':             args
		})

