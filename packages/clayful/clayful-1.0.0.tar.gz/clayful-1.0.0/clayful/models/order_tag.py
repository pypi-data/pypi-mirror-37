class OrderTag:

	Clayful = None
	name = 'OrderTag'
	path = 'orders/tags'

	@staticmethod
	def config(clayful):

		OrderTag.Clayful = clayful

		return OrderTag

	@staticmethod
	def list(*args):

		return OrderTag.Clayful.call_api({
			'model_name':       OrderTag.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/orders/tags',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return OrderTag.Clayful.call_api({
			'model_name':       OrderTag.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/orders/tags/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return OrderTag.Clayful.call_api({
			'model_name':       OrderTag.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/orders/tags/{orderTagId}',
			'params':           ('orderTagId', ),
			'args':             args
		})

