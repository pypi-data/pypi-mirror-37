class Catalog:

	Clayful = None
	name = 'Catalog'
	path = 'catalogs'

	@staticmethod
	def config(clayful):

		Catalog.Clayful = clayful

		return Catalog

	@staticmethod
	def list(*args):

		return Catalog.Clayful.call_api({
			'model_name':       Catalog.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/catalogs',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Catalog.Clayful.call_api({
			'model_name':       Catalog.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/catalogs/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Catalog.Clayful.call_api({
			'model_name':       Catalog.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/catalogs/{catalogId}',
			'params':           ('catalogId', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Catalog.Clayful.call_api({
			'model_name':       Catalog.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/catalogs/{catalogId}/meta/{field}/pull',
			'params':           ('catalogId', 'field', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Catalog.Clayful.call_api({
			'model_name':       Catalog.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/catalogs/{catalogId}/meta/{field}/inc',
			'params':           ('catalogId', 'field', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Catalog.Clayful.call_api({
			'model_name':       Catalog.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/catalogs/{catalogId}/meta/{field}/push',
			'params':           ('catalogId', 'field', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Catalog.Clayful.call_api({
			'model_name':       Catalog.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/catalogs/{catalogId}/meta/{field}',
			'params':           ('catalogId', 'field', ),
			'args':             args
		})

