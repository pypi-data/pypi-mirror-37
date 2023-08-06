class ShippingMethod:

	Clayful = None
	name = 'ShippingMethod'
	path = 'shipping/methods'

	@staticmethod
	def config(clayful):

		ShippingMethod.Clayful = clayful

		return ShippingMethod

	@staticmethod
	def list(*args):

		return ShippingMethod.Clayful.call_api({
			'model_name':       ShippingMethod.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/shipping/methods',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return ShippingMethod.Clayful.call_api({
			'model_name':       ShippingMethod.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/shipping/methods/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return ShippingMethod.Clayful.call_api({
			'model_name':       ShippingMethod.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/shipping/methods/{shippingMethodId}',
			'params':           ('shippingMethodId', ),
			'args':             args
		})

