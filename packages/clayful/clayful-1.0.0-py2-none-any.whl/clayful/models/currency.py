class Currency:

	Clayful = None
	name = 'Currency'
	path = 'currencies'

	@staticmethod
	def config(clayful):

		Currency.Clayful = clayful

		return Currency

	@staticmethod
	def list(*args):

		return Currency.Clayful.call_api({
			'model_name':       Currency.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/currencies',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Currency.Clayful.call_api({
			'model_name':       Currency.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/currencies/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Currency.Clayful.call_api({
			'model_name':       Currency.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/currencies/{currencyId}',
			'params':           ('currencyId', ),
			'args':             args
		})

