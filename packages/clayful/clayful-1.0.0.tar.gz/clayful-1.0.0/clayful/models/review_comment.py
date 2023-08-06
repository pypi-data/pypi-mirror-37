class ReviewComment:

	Clayful = None
	name = 'ReviewComment'
	path = 'products/reviews/comments'

	@staticmethod
	def config(clayful):

		ReviewComment.Clayful = clayful

		return ReviewComment

	@staticmethod
	def list(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/products/reviews/comments',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/products/reviews/comments/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/products/reviews/comments/{reviewCommentId}',
			'params':           ('reviewCommentId', ),
			'args':             args
		})

	@staticmethod
	def create(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'create',
			'http_method':      'POST',
			'path':             '/v1/products/reviews/comments',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def create_for_me(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'create_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/products/reviews/comments',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def flag(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'flag',
			'http_method':      'POST',
			'path':             '/v1/products/reviews/comments/{reviewCommentId}/flags',
			'params':           ('reviewCommentId', ),
			'args':             args
		})

	@staticmethod
	def flag_for_me(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'flag_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/products/reviews/comments/{reviewCommentId}/flags',
			'params':           ('reviewCommentId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/reviews/comments/{reviewCommentId}/meta/{field}/push',
			'params':           ('reviewCommentId', 'field', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/reviews/comments/{reviewCommentId}/meta/{field}/pull',
			'params':           ('reviewCommentId', 'field', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/reviews/comments/{reviewCommentId}/meta/{field}/inc',
			'params':           ('reviewCommentId', 'field', ),
			'args':             args
		})

	@staticmethod
	def update(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'update',
			'http_method':      'PUT',
			'path':             '/v1/products/reviews/comments/{reviewCommentId}',
			'params':           ('reviewCommentId', ),
			'args':             args
		})

	@staticmethod
	def update_for_me(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'update_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/products/reviews/comments/{reviewCommentId}',
			'params':           ('reviewCommentId', ),
			'args':             args
		})

	@staticmethod
	def delete(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'delete',
			'http_method':      'DELETE',
			'path':             '/v1/products/reviews/comments/{reviewCommentId}',
			'params':           ('reviewCommentId', ),
			'args':             args
		})

	@staticmethod
	def delete_for_me(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'delete_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/products/reviews/comments/{reviewCommentId}',
			'params':           ('reviewCommentId', ),
			'args':             args
		})

	@staticmethod
	def cancel_flag_for_me(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'cancel_flag_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/products/reviews/comments/{reviewCommentId}/flags',
			'params':           ('reviewCommentId', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/products/reviews/comments/{reviewCommentId}/meta/{field}',
			'params':           ('reviewCommentId', 'field', ),
			'args':             args
		})

	@staticmethod
	def cancel_flag(*args):

		return ReviewComment.Clayful.call_api({
			'model_name':       ReviewComment.name,
			'method_name':      'cancel_flag',
			'http_method':      'DELETE',
			'path':             '/v1/products/reviews/comments/{reviewCommentId}/flags/{customerId}',
			'params':           ('reviewCommentId', 'customerId', ),
			'args':             args
		})

