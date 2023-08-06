class PaymentMethod:

	Clayful = None
	name = 'PaymentMethod'
	path = 'payments/methods'

	@staticmethod
	def config(clayful):

		PaymentMethod.Clayful = clayful

		return PaymentMethod

	@staticmethod
	def list(*args):

		return PaymentMethod.Clayful.call_api({
			'model_name':       PaymentMethod.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/payments/methods',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return PaymentMethod.Clayful.call_api({
			'model_name':       PaymentMethod.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/payments/methods/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return PaymentMethod.Clayful.call_api({
			'model_name':       PaymentMethod.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/payments/methods/{paymentMethodId}',
			'params':           ('paymentMethodId', ),
			'args':             args
		})

