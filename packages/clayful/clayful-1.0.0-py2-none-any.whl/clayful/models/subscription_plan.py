class SubscriptionPlan:

	Clayful = None
	name = 'SubscriptionPlan'
	path = 'subscriptions/plans'

	@staticmethod
	def config(clayful):

		SubscriptionPlan.Clayful = clayful

		return SubscriptionPlan

	@staticmethod
	def list(*args):

		return SubscriptionPlan.Clayful.call_api({
			'model_name':       SubscriptionPlan.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/subscriptions/plans',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return SubscriptionPlan.Clayful.call_api({
			'model_name':       SubscriptionPlan.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/subscriptions/plans/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return SubscriptionPlan.Clayful.call_api({
			'model_name':       SubscriptionPlan.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/subscriptions/plans/{subscriptionPlanId}',
			'params':           ('subscriptionPlanId', ),
			'args':             args
		})

