class Subscription:

	Clayful = None
	name = 'Subscription'
	path = 'subscriptions'

	@staticmethod
	def config(clayful):

		Subscription.Clayful = clayful

		return Subscription

	@staticmethod
	def list(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/subscriptions',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def list_for_me(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'list_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/subscriptions',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/subscriptions/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/subscriptions/{subscriptionId}',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def count_for_me(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'count_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/subscriptions/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get_for_me(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'get_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/subscriptions/{subscriptionId}',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def list_inventory_operations(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'list_inventory_operations',
			'http_method':      'GET',
			'path':             '/v1/subscriptions/{subscriptionId}/inventory/operations',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def sync_inventory(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'sync_inventory',
			'http_method':      'POST',
			'path':             '/v1/subscriptions/{subscriptionId}/synced',
			'params':           ('subscriptionId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def authenticate(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'authenticate',
			'http_method':      'POST',
			'path':             '/v1/subscriptions/{subscriptionId}/auth',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def cancel(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'cancel',
			'http_method':      'POST',
			'path':             '/v1/subscriptions/{subscriptionId}/cancellation',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def mark_as_done(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'mark_as_done',
			'http_method':      'POST',
			'path':             '/v1/subscriptions/{subscriptionId}/done',
			'params':           ('subscriptionId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def schedule(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'schedule',
			'http_method':      'POST',
			'path':             '/v1/subscriptions/{subscriptionId}/scheduled',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def schedule_for_me(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'schedule_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/subscriptions/{subscriptionId}/scheduled',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def cancel_for_me(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'cancel_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/subscriptions/{subscriptionId}/cancellation',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def fulfill_schedule(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'fulfill_schedule',
			'http_method':      'POST',
			'path':             '/v1/subscriptions/{subscriptionId}/schedules/orders',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/subscriptions/{subscriptionId}/meta/{field}/pull',
			'params':           ('subscriptionId', 'field', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/subscriptions/{subscriptionId}/meta/{field}/inc',
			'params':           ('subscriptionId', 'field', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/subscriptions/{subscriptionId}/meta/{field}/push',
			'params':           ('subscriptionId', 'field', ),
			'args':             args
		})

	@staticmethod
	def update(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'update',
			'http_method':      'PUT',
			'path':             '/v1/subscriptions/{subscriptionId}',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def update_for_me(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'update_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/subscriptions/{subscriptionId}',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def update_cancellation(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'update_cancellation',
			'http_method':      'PUT',
			'path':             '/v1/subscriptions/{subscriptionId}/cancellation',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def update_cancellation_for_me(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'update_cancellation_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/subscriptions/{subscriptionId}/cancellation',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def delete(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'delete',
			'http_method':      'DELETE',
			'path':             '/v1/subscriptions/{subscriptionId}',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def mark_as_undone(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'mark_as_undone',
			'http_method':      'DELETE',
			'path':             '/v1/subscriptions/{subscriptionId}/done',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/subscriptions/{subscriptionId}/meta/{field}',
			'params':           ('subscriptionId', 'field', ),
			'args':             args
		})

	@staticmethod
	def delete_inventory_operation(*args):

		return Subscription.Clayful.call_api({
			'model_name':       Subscription.name,
			'method_name':      'delete_inventory_operation',
			'http_method':      'DELETE',
			'path':             '/v1/subscriptions/{subscriptionId}/inventory/operations/{operationId}',
			'params':           ('subscriptionId', 'operationId', ),
			'args':             args
		})

