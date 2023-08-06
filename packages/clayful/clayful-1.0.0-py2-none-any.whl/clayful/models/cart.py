class Cart:

	Clayful = None
	name = 'Cart'
	path = ''

	@staticmethod
	def config(clayful):

		Cart.Clayful = clayful

		return Cart

	@staticmethod
	def count_items_for_me(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'count_items_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/cart/items/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count_items(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'count_items',
			'http_method':      'GET',
			'path':             '/v1/customers/{customerId}/cart/items/count',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def get_for_me(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'get_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/cart',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get_as_non_registered(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'get_as_non_registered',
			'http_method':      'POST',
			'path':             '/v1/customers/non-registered/cart',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'get',
			'http_method':      'POST',
			'path':             '/v1/customers/{customerId}/cart',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def add_item_for_me(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'add_item_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/cart/items',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get_as_non_registered_for_me(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'get_as_non_registered_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/non-registered/cart',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def add_item(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'add_item',
			'http_method':      'POST',
			'path':             '/v1/customers/{customerId}/cart/items',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def checkout_for_me(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'checkout_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/cart/checkout/{type}',
			'params':           ('type', ),
			'args':             args
		})

	@staticmethod
	def checkout_as_non_registered(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'checkout_as_non_registered',
			'http_method':      'POST',
			'path':             '/v1/customers/non-registered/cart/checkout/{type}',
			'params':           ('type', ),
			'args':             args
		})

	@staticmethod
	def checkout(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'checkout',
			'http_method':      'POST',
			'path':             '/v1/customers/{customerId}/cart/checkout/{type}',
			'params':           ('customerId', 'type', ),
			'args':             args
		})

	@staticmethod
	def checkout_as_non_registered_for_me(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'checkout_as_non_registered_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/non-registered/cart/checkout/{type}',
			'params':           ('type', ),
			'args':             args
		})

	@staticmethod
	def update_item_for_me(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'update_item_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/cart/items/{itemId}',
			'params':           ('itemId', ),
			'args':             args
		})

	@staticmethod
	def update_item(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'update_item',
			'http_method':      'PUT',
			'path':             '/v1/customers/{customerId}/cart/items/{itemId}',
			'params':           ('customerId', 'itemId', ),
			'args':             args
		})

	@staticmethod
	def empty_for_me(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'empty_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/cart/items',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def empty(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'empty',
			'http_method':      'DELETE',
			'path':             '/v1/customers/{customerId}/cart/items',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def delete_item_for_me(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'delete_item_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/cart/items/{itemId}',
			'params':           ('itemId', ),
			'args':             args
		})

	@staticmethod
	def delete_item(*args):

		return Cart.Clayful.call_api({
			'model_name':       Cart.name,
			'method_name':      'delete_item',
			'http_method':      'DELETE',
			'path':             '/v1/customers/{customerId}/cart/items/{itemId}',
			'params':           ('customerId', 'itemId', ),
			'args':             args
		})

