class Review:

	Clayful = None
	name = 'Review'
	path = 'products/reviews'

	@staticmethod
	def config(clayful):

		Review.Clayful = clayful

		return Review

	@staticmethod
	def list(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/products/reviews',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/products/reviews/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def list_published(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'list_published',
			'http_method':      'GET',
			'path':             '/v1/products/reviews/published',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/products/reviews/{reviewId}',
			'params':           ('reviewId', ),
			'args':             args
		})

	@staticmethod
	def count_published(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'count_published',
			'http_method':      'GET',
			'path':             '/v1/products/reviews/published/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get_published(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'get_published',
			'http_method':      'GET',
			'path':             '/v1/products/reviews/published/{reviewId}',
			'params':           ('reviewId', ),
			'args':             args
		})

	@staticmethod
	def create(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'create',
			'http_method':      'POST',
			'path':             '/v1/products/reviews',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def create_for_me(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'create_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/products/reviews',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def flag(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'flag',
			'http_method':      'POST',
			'path':             '/v1/products/reviews/{reviewId}/flags',
			'params':           ('reviewId', ),
			'args':             args
		})

	@staticmethod
	def flag_for_me(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'flag_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/products/reviews/{reviewId}/flags',
			'params':           ('reviewId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def helped(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'helped',
			'http_method':      'POST',
			'path':             '/v1/products/reviews/{reviewId}/helped/{upDown}',
			'params':           ('reviewId', 'upDown', ),
			'args':             args
		})

	@staticmethod
	def helped_for_me(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'helped_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/products/reviews/{reviewId}/helped/{upDown}',
			'params':           ('reviewId', 'upDown', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/reviews/{reviewId}/meta/{field}/pull',
			'params':           ('reviewId', 'field', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/reviews/{reviewId}/meta/{field}/inc',
			'params':           ('reviewId', 'field', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/reviews/{reviewId}/meta/{field}/push',
			'params':           ('reviewId', 'field', ),
			'args':             args
		})

	@staticmethod
	def update(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'update',
			'http_method':      'PUT',
			'path':             '/v1/products/reviews/{reviewId}',
			'params':           ('reviewId', ),
			'args':             args
		})

	@staticmethod
	def update_for_me(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'update_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/products/reviews/{reviewId}',
			'params':           ('reviewId', ),
			'args':             args
		})

	@staticmethod
	def delete(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'delete',
			'http_method':      'DELETE',
			'path':             '/v1/products/reviews/{reviewId}',
			'params':           ('reviewId', ),
			'args':             args
		})

	@staticmethod
	def delete_for_me(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'delete_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/products/reviews/{reviewId}',
			'params':           ('reviewId', ),
			'args':             args
		})

	@staticmethod
	def cancel_flag_for_me(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'cancel_flag_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/products/reviews/{reviewId}/flags',
			'params':           ('reviewId', ),
			'args':             args
		})

	@staticmethod
	def cancel_flag(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'cancel_flag',
			'http_method':      'DELETE',
			'path':             '/v1/products/reviews/{reviewId}/flags/{customerId}',
			'params':           ('reviewId', 'customerId', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/products/reviews/{reviewId}/meta/{field}',
			'params':           ('reviewId', 'field', ),
			'args':             args
		})

	@staticmethod
	def cancel_helped_for_me(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'cancel_helped_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/products/reviews/{reviewId}/helped/{upDown}',
			'params':           ('reviewId', 'upDown', ),
			'args':             args
		})

	@staticmethod
	def cancel_helped(*args):

		return Review.Clayful.call_api({
			'model_name':       Review.name,
			'method_name':      'cancel_helped',
			'http_method':      'DELETE',
			'path':             '/v1/products/reviews/{reviewId}/helped/{upDown}/{customerId}',
			'params':           ('reviewId', 'upDown', 'customerId', ),
			'args':             args
		})

