class Customer:

	Clayful = None
	name = 'Customer'
	path = 'customers'

	@staticmethod
	def config(clayful):

		Customer.Clayful = clayful

		return Customer

	@staticmethod
	def list(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/customers',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get_me(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'get_me',
			'http_method':      'GET',
			'path':             '/v1/me',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def is_authenticated(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'is_authenticated',
			'http_method':      'GET',
			'path':             '/v1/customers/auth',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/customers/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/customers/{customerId}',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def list_coupons_for_me(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'list_coupons_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/coupons',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def list_coupons(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'list_coupons',
			'http_method':      'GET',
			'path':             '/v1/customers/{customerId}/coupons',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def count_coupons_for_me(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'count_coupons_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/coupons/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count_coupons(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'count_coupons',
			'http_method':      'GET',
			'path':             '/v1/customers/{customerId}/coupons/count',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def list_by_flag_votes(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'list_by_flag_votes',
			'http_method':      'GET',
			'path':             '/v1/{voteModel}/{voteModelId}/flags/customers',
			'params':           ('voteModel', 'voteModelId', ),
			'args':             args
		})

	@staticmethod
	def list_by_help_votes(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'list_by_help_votes',
			'http_method':      'GET',
			'path':             '/v1/{voteModel}/{voteModelId}/helped/{upDown}/customers',
			'params':           ('voteModel', 'voteModelId', 'upDown', ),
			'args':             args
		})

	@staticmethod
	def list_by_flag_votes(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'list_by_flag_votes',
			'http_method':      'GET',
			'path':             '/v1/{voteModel}/{voteModelId}/flags/customers',
			'params':           ('voteModel', 'voteModelId', ),
			'args':             args
		})

	@staticmethod
	def list_by_help_votes(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'list_by_help_votes',
			'http_method':      'GET',
			'path':             '/v1/{voteModel}/{voteModelId}/helped/{upDown}/customers',
			'params':           ('voteModel', 'voteModelId', 'upDown', ),
			'args':             args
		})

	@staticmethod
	def create(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'create',
			'http_method':      'POST',
			'path':             '/v1/customers',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def create_me(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'create_me',
			'http_method':      'POST',
			'path':             '/v1/me',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def authenticate(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'authenticate',
			'http_method':      'POST',
			'path':             '/v1/customers/auth',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def create_verification(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'create_verification',
			'http_method':      'POST',
			'path':             '/v1/customers/verifications',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def authenticate_by_3rd_party(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'authenticate_by_3rd_party',
			'http_method':      'POST',
			'path':             '/v1/customers/auth/{vendor}',
			'params':           ('vendor', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def request_verification_email(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'request_verification_email',
			'http_method':      'POST',
			'path':             '/v1/customers/verifications/emails',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def add_coupon(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'add_coupon',
			'http_method':      'POST',
			'path':             '/v1/customers/{customerId}/coupons',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def verify(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'verify',
			'http_method':      'POST',
			'path':             '/v1/customers/{customerId}/verified',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/customers/{customerId}/meta/{field}/push',
			'params':           ('customerId', 'field', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/customers/{customerId}/meta/{field}/inc',
			'params':           ('customerId', 'field', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/customers/{customerId}/meta/{field}/pull',
			'params':           ('customerId', 'field', ),
			'args':             args
		})

	@staticmethod
	def update_me(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'update_me',
			'http_method':      'PUT',
			'path':             '/v1/me',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def update(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'update',
			'http_method':      'PUT',
			'path':             '/v1/customers/{customerId}',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def update_credentials_for_me(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'update_credentials_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/credentials',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def reset_password(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'reset_password',
			'http_method':      'PUT',
			'path':             '/v1/customers/{customerId}/password',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def update_credentials(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'update_credentials',
			'http_method':      'PUT',
			'path':             '/v1/customers/{customerId}/credentials',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def delete_me(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'delete_me',
			'http_method':      'DELETE',
			'path':             '/v1/me',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def delete(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'delete',
			'http_method':      'DELETE',
			'path':             '/v1/customers/{customerId}',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def delete_coupon_for_me(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'delete_coupon_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/coupons/{couponId}',
			'params':           ('couponId', ),
			'args':             args
		})

	@staticmethod
	def delete_coupon(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'delete_coupon',
			'http_method':      'DELETE',
			'path':             '/v1/customers/{customerId}/coupons/{couponId}',
			'params':           ('customerId', 'couponId', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Customer.Clayful.call_api({
			'model_name':       Customer.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/customers/{customerId}/meta/{field}',
			'params':           ('customerId', 'field', ),
			'args':             args
		})

