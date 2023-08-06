class Impression:

	Clayful = None
	name = 'Impression'
	path = ''

	@staticmethod
	def config(clayful):

		Impression.Clayful = clayful

		return Impression

	@staticmethod
	def top_brands(*args):

		return Impression.Clayful.call_api({
			'model_name':       Impression.name,
			'method_name':      'top_brands',
			'http_method':      'GET',
			'path':             '/v1/impressions/{scope}/top/brands',
			'params':           ('scope', ),
			'args':             args
		})

	@staticmethod
	def top_products(*args):

		return Impression.Clayful.call_api({
			'model_name':       Impression.name,
			'method_name':      'top_products',
			'http_method':      'GET',
			'path':             '/v1/impressions/{scope}/top/products',
			'params':           ('scope', ),
			'args':             args
		})

	@staticmethod
	def top_collections(*args):

		return Impression.Clayful.call_api({
			'model_name':       Impression.name,
			'method_name':      'top_collections',
			'http_method':      'GET',
			'path':             '/v1/impressions/{scope}/top/collections',
			'params':           ('scope', ),
			'args':             args
		})

	@staticmethod
	def gather(*args):

		return Impression.Clayful.call_api({
			'model_name':       Impression.name,
			'method_name':      'gather',
			'http_method':      'POST',
			'path':             '/v1/impressions/{scope}',
			'params':           ('scope', ),
			'args':             args
		})

