class Store:

	Clayful = None
	name = 'Store'
	path = 'store'

	@staticmethod
	def config(clayful):

		Store.Clayful = clayful

		return Store

	@staticmethod
	def get(*args):

		return Store.Clayful.call_api({
			'model_name':       Store.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/store',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Store.Clayful.call_api({
			'model_name':       Store.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/store/meta/{field}/pull',
			'params':           ('field', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Store.Clayful.call_api({
			'model_name':       Store.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/store/meta/{field}/inc',
			'params':           ('field', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Store.Clayful.call_api({
			'model_name':       Store.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/store/meta/{field}/push',
			'params':           ('field', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Store.Clayful.call_api({
			'model_name':       Store.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/store/meta/{field}',
			'params':           ('field', ),
			'args':             args
		})

