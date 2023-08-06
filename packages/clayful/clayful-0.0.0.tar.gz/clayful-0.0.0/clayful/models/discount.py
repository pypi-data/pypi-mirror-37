class Discount:

	Clayful = None
	name = 'Discount'
	path = 'discounts'

	@staticmethod
	def config(clayful):

		Discount.Clayful = clayful

		return Discount

	@staticmethod
	def list(*args):

		return Discount.Clayful.call_api({
			'model_name':       Discount.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/discounts',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Discount.Clayful.call_api({
			'model_name':       Discount.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/discounts/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Discount.Clayful.call_api({
			'model_name':       Discount.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/discounts/{discountId}',
			'params':           ('discountId', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Discount.Clayful.call_api({
			'model_name':       Discount.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/discounts/{discountId}/meta/{field}/push',
			'params':           ('discountId', 'field', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Discount.Clayful.call_api({
			'model_name':       Discount.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/discounts/{discountId}/meta/{field}/inc',
			'params':           ('discountId', 'field', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Discount.Clayful.call_api({
			'model_name':       Discount.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/discounts/{discountId}/meta/{field}/pull',
			'params':           ('discountId', 'field', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Discount.Clayful.call_api({
			'model_name':       Discount.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/discounts/{discountId}/meta/{field}',
			'params':           ('discountId', 'field', ),
			'args':             args
		})

