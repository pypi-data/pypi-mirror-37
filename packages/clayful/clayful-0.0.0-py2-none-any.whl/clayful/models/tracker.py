class Tracker:

	Clayful = None
	name = 'Tracker'
	path = ''

	@staticmethod
	def config(clayful):

		Tracker.Clayful = clayful

		return Tracker

	@staticmethod
	def get_by_customer_for_me(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'get_by_customer_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/tracker',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/trackers/{trackerId}',
			'params':           ('trackerId', ),
			'args':             args
		})

	@staticmethod
	def get_by_customer(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'get_by_customer',
			'http_method':      'GET',
			'path':             '/v1/customers/{customerId}/tracker',
			'params':           ('customerId', ),
			'args':             args
		})

	@staticmethod
	def get_for_me(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'get_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/trackers/{trackerId}',
			'params':           ('trackerId', ),
			'args':             args
		})

	@staticmethod
	def get_as_non_registered_for_me(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'get_as_non_registered_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/non-registered/trackers/{trackerId}',
			'params':           ('trackerId', ),
			'args':             args
		})

	@staticmethod
	def create(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'create',
			'http_method':      'POST',
			'path':             '/v1/trackers',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def create_for_me(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'create_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/trackers',
			'params':           (),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def create_as_non_registered_for_me(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'create_as_non_registered_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/non-registered/trackers',
			'params':           (),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def change_owner(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'change_owner',
			'http_method':      'PUT',
			'path':             '/v1/trackers/{trackerId}/customer',
			'params':           ('trackerId', ),
			'args':             args
		})

	@staticmethod
	def change_owner_for_me(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'change_owner_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/trackers/{trackerId}/customer',
			'params':           ('trackerId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def delete(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'delete',
			'http_method':      'DELETE',
			'path':             '/v1/trackers/{trackerId}',
			'params':           ('trackerId', ),
			'args':             args
		})

	@staticmethod
	def delete_for_me(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'delete_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/trackers/{trackerId}',
			'params':           ('trackerId', ),
			'args':             args
		})

	@staticmethod
	def delete_as_non_registered_for_me(*args):

		return Tracker.Clayful.call_api({
			'model_name':       Tracker.name,
			'method_name':      'delete_as_non_registered_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/non-registered/trackers/{trackerId}',
			'params':           ('trackerId', ),
			'args':             args
		})

