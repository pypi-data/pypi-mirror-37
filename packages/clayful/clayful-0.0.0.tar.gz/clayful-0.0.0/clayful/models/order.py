class Order:

	Clayful = None
	name = 'Order'
	path = 'orders'

	@staticmethod
	def config(clayful):

		Order.Clayful = clayful

		return Order

	@staticmethod
	def list(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/orders',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def list_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'list_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/orders',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/orders/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/orders/{orderId}',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def count_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'count_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/orders/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'get_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/orders/{orderId}',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def list_by_subscription(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'list_by_subscription',
			'http_method':      'GET',
			'path':             '/v1/subscriptions/{subscriptionId}/orders',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def list_by_subscription_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'list_by_subscription_for_me',
			'http_method':      'GET',
			'path':             '/v1/me/subscriptions/{subscriptionId}/orders',
			'params':           ('subscriptionId', ),
			'args':             args
		})

	@staticmethod
	def list_inventory_operations(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'list_inventory_operations',
			'http_method':      'GET',
			'path':             '/v1/orders/{orderId}/inventory/operations',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def authenticate(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'authenticate',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/auth',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def mark_as_received(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'mark_as_received',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/received',
			'params':           ('orderId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def mark_as_done(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'mark_as_done',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/done',
			'params':           ('orderId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def sync_inventory(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'sync_inventory',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/synced',
			'params':           ('orderId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def create_fulfillment(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'create_fulfillment',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/fulfillments',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def request_refund(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'request_refund',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/refunds',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def cancel(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'cancel',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/cancellation',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def cancel_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'cancel_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/orders/{orderId}/cancellation',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def mark_as_received_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'mark_as_received_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/orders/{orderId}/received',
			'params':           ('orderId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def request_refund_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'request_refund_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/orders/{orderId}/refunds',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def check_ticket(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'check_ticket',
			'http_method':      'POST',
			'path':             '/v1/orders/tickets/{code}/validity',
			'params':           ('code', ),
			'args':             args
		})

	@staticmethod
	def use_ticket(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'use_ticket',
			'http_method':      'POST',
			'path':             '/v1/orders/tickets/{code}/used',
			'params':           ('code', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def accept_refund(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'accept_refund',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/refunds/{refundId}/accepted',
			'params':           ('orderId', 'refundId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def restock_refund_items(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'restock_refund_items',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/refunds/{refundId}/restock',
			'params':           ('orderId', 'refundId', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/meta/{field}/inc',
			'params':           ('orderId', 'field', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/meta/{field}/pull',
			'params':           ('orderId', 'field', ),
			'args':             args
		})

	@staticmethod
	def cancel_refund(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'cancel_refund',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/refunds/{refundId}/cancellation',
			'params':           ('orderId', 'refundId', ),
			'args':             args
		})

	@staticmethod
	def register_payment_method(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'register_payment_method',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/transactions/payments/methods',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/meta/{field}/push',
			'params':           ('orderId', 'field', ),
			'args':             args
		})

	@staticmethod
	def cancel_refund_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'cancel_refund_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/orders/{orderId}/refunds/{refundId}/cancellation',
			'params':           ('orderId', 'refundId', ),
			'args':             args
		})

	@staticmethod
	def create_download_url(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'create_download_url',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/items/{itemId}/download/url',
			'params':           ('orderId', 'itemId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def restock_all_refund_items(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'restock_all_refund_items',
			'http_method':      'POST',
			'path':             '/v1/orders/{orderId}/refunds/{refundId}/restock/all',
			'params':           ('orderId', 'refundId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def create_download_url_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'create_download_url_for_me',
			'http_method':      'POST',
			'path':             '/v1/me/orders/{orderId}/items/{itemId}/download/url',
			'params':           ('orderId', 'itemId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def update(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update',
			'http_method':      'PUT',
			'path':             '/v1/orders/{orderId}',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def update_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/orders/{orderId}',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def update_transactions(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_transactions',
			'http_method':      'PUT',
			'path':             '/v1/orders/{orderId}/transactions',
			'params':           ('orderId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def update_cancellation(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_cancellation',
			'http_method':      'PUT',
			'path':             '/v1/orders/{orderId}/cancellation',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def update_cancellation_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_cancellation_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/orders/{orderId}/cancellation',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def update_transactions_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_transactions_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/orders/{orderId}/transactions',
			'params':           ('orderId', ),
			'without_payload':  True,
			'args':             args
		})

	@staticmethod
	def update_refund(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_refund',
			'http_method':      'PUT',
			'path':             '/v1/orders/{orderId}/refunds/{refundId}',
			'params':           ('orderId', 'refundId', ),
			'args':             args
		})

	@staticmethod
	def update_fulfillment(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_fulfillment',
			'http_method':      'PUT',
			'path':             '/v1/orders/{orderId}/fulfillments/{fulfillmentId}',
			'params':           ('orderId', 'fulfillmentId', ),
			'args':             args
		})

	@staticmethod
	def update_item(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_item',
			'http_method':      'PUT',
			'path':             '/v1/orders/{orderId}/items/{itemId}',
			'params':           ('orderId', 'itemId', ),
			'args':             args
		})

	@staticmethod
	def update_refund_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_refund_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/orders/{orderId}/refunds/{refundId}',
			'params':           ('orderId', 'refundId', ),
			'args':             args
		})

	@staticmethod
	def update_refund_cancellation(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_refund_cancellation',
			'http_method':      'PUT',
			'path':             '/v1/orders/{orderId}/refunds/{refundId}/cancellation',
			'params':           ('orderId', 'refundId', ),
			'args':             args
		})

	@staticmethod
	def update_refund_cancellation_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'update_refund_cancellation_for_me',
			'http_method':      'PUT',
			'path':             '/v1/me/orders/{orderId}/refunds/{refundId}/cancellation',
			'params':           ('orderId', 'refundId', ),
			'args':             args
		})

	@staticmethod
	def delete(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'delete',
			'http_method':      'DELETE',
			'path':             '/v1/orders/{orderId}',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def mark_as_undone(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'mark_as_undone',
			'http_method':      'DELETE',
			'path':             '/v1/orders/{orderId}/done',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def mark_as_not_received(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'mark_as_not_received',
			'http_method':      'DELETE',
			'path':             '/v1/orders/{orderId}/received',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def mark_as_not_received_for_me(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'mark_as_not_received_for_me',
			'http_method':      'DELETE',
			'path':             '/v1/me/orders/{orderId}/received',
			'params':           ('orderId', ),
			'args':             args
		})

	@staticmethod
	def delete_fulfillment(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'delete_fulfillment',
			'http_method':      'DELETE',
			'path':             '/v1/orders/{orderId}/fulfillments/{fulfillmentId}',
			'params':           ('orderId', 'fulfillmentId', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/orders/{orderId}/meta/{field}',
			'params':           ('orderId', 'field', ),
			'args':             args
		})

	@staticmethod
	def delete_refund(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'delete_refund',
			'http_method':      'DELETE',
			'path':             '/v1/orders/{orderId}/refunds/{refundId}',
			'params':           ('orderId', 'refundId', ),
			'args':             args
		})

	@staticmethod
	def delete_inventory_operation(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'delete_inventory_operation',
			'http_method':      'DELETE',
			'path':             '/v1/orders/{orderId}/inventory/operations/{operationId}',
			'params':           ('orderId', 'operationId', ),
			'args':             args
		})

	@staticmethod
	def unaccept_refund(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'unaccept_refund',
			'http_method':      'DELETE',
			'path':             '/v1/orders/{orderId}/refunds/{refundId}/accepted',
			'params':           ('orderId', 'refundId', ),
			'args':             args
		})

	@staticmethod
	def unregister_payment_method(*args):

		return Order.Clayful.call_api({
			'model_name':       Order.name,
			'method_name':      'unregister_payment_method',
			'http_method':      'DELETE',
			'path':             '/v1/orders/{orderId}/transactions/payments/methods/{paymentMethodId}',
			'params':           ('orderId', 'paymentMethodId', ),
			'args':             args
		})

