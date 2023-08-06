class Coupon:

	Clayful = None
	name = 'Coupon'
	path = 'coupons'

	@staticmethod
	def config(clayful):

		Coupon.Clayful = clayful

		return Coupon

	@staticmethod
	def list(*args):

		return Coupon.Clayful.call_api({
			'model_name':       Coupon.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/coupons',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Coupon.Clayful.call_api({
			'model_name':       Coupon.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/coupons/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Coupon.Clayful.call_api({
			'model_name':       Coupon.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/coupons/{couponId}',
			'params':           ('couponId', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Coupon.Clayful.call_api({
			'model_name':       Coupon.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/coupons/{couponId}/meta/{field}/pull',
			'params':           ('couponId', 'field', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Coupon.Clayful.call_api({
			'model_name':       Coupon.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/coupons/{couponId}/meta/{field}/inc',
			'params':           ('couponId', 'field', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Coupon.Clayful.call_api({
			'model_name':       Coupon.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/coupons/{couponId}/meta/{field}/push',
			'params':           ('couponId', 'field', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Coupon.Clayful.call_api({
			'model_name':       Coupon.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/coupons/{couponId}/meta/{field}',
			'params':           ('couponId', 'field', ),
			'args':             args
		})

