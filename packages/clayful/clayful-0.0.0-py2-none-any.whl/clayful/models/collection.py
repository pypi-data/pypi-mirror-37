class Collection:

	Clayful = None
	name = 'Collection'
	path = 'collections'

	@staticmethod
	def config(clayful):

		Collection.Clayful = clayful

		return Collection

	@staticmethod
	def list(*args):

		return Collection.Clayful.call_api({
			'model_name':       Collection.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/collections',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Collection.Clayful.call_api({
			'model_name':       Collection.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/collections/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Collection.Clayful.call_api({
			'model_name':       Collection.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/collections/{collectionId}',
			'params':           ('collectionId', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Collection.Clayful.call_api({
			'model_name':       Collection.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/collections/{collectionId}/meta/{field}/push',
			'params':           ('collectionId', 'field', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Collection.Clayful.call_api({
			'model_name':       Collection.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/collections/{collectionId}/meta/{field}/inc',
			'params':           ('collectionId', 'field', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Collection.Clayful.call_api({
			'model_name':       Collection.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/collections/{collectionId}/meta/{field}/pull',
			'params':           ('collectionId', 'field', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Collection.Clayful.call_api({
			'model_name':       Collection.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/collections/{collectionId}/meta/{field}',
			'params':           ('collectionId', 'field', ),
			'args':             args
		})

