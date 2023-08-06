class Image:

	Clayful = None
	name = 'Image'
	path = 'images'

	@staticmethod
	def config(clayful):

		Image.Clayful = clayful

		return Image

	@staticmethod
	def list(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/images',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/images/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/images/{imageId}',
			'params':           ('imageId', ),
			'args':             args
		})

	@staticmethod
	def list_for_me(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'list_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/images',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count_for_me(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'count_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/images/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get_for_me(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'get_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/images/{imageId}',
			'params':           ('imageId', ),
			'args':             args
		})

	@staticmethod
	def create(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'create',
			'http_method':      'POST',
			'path':             '/v1/images',
			'params':           (),
			'uses_form_data':   True,
			'args':             args
		})

	@staticmethod
	def create_for_me(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'create_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/images',
			'params':           (),
			'uses_form_data':   True,
			'args':             args
		})

	@staticmethod
	def create_as_customer(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'create_as_customer',
			'http_method':      'POST',
			'path':             '/v1/customers/{customerId}/images',
			'params':           ('customerId', ),
			'uses_form_data':   True,
			'args':             args
		})

	@staticmethod
	def update(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'update',
			'http_method':      'PUT',
			'path':             '/v1/images/{imageId}',
			'params':           ('imageId', ),
			'uses_form_data':   True,
			'args':             args
		})

	@staticmethod
	def update_for_me(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'update_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/images/{imageId}',
			'params':           ('imageId', ),
			'uses_form_data':   True,
			'args':             args
		})

	@staticmethod
	def update_as_customer(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'update_as_customer',
			'http_method':      'PUT',
			'path':             '/v1/customers/{customerId}/images/{imageId}',
			'params':           ('customerId', 'imageId', ),
			'uses_form_data':   True,
			'args':             args
		})

	@staticmethod
	def delete(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'delete',
			'http_method':      'DELETE',
			'path':             '/v1/images/{imageId}',
			'params':           ('imageId', ),
			'args':             args
		})

	@staticmethod
	def delete_for_me(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'delete_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/images/{imageId}',
			'params':           ('imageId', ),
			'args':             args
		})

	@staticmethod
	def delete_as_customer(*args):

		return Image.Clayful.call_api({
			'model_name':       Image.name,
			'method_name':      'delete_as_customer',
			'http_method':      'DELETE',
			'path':             '/v1/customers/{customerId}/images/{imageId}',
			'params':           ('customerId', 'imageId', ),
			'args':             args
		})

