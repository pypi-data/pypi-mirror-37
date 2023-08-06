class TaxCategory:

	Clayful = None
	name = 'TaxCategory'
	path = 'taxes/categories'

	@staticmethod
	def config(clayful):

		TaxCategory.Clayful = clayful

		return TaxCategory

	@staticmethod
	def list(*args):

		return TaxCategory.Clayful.call_api({
			'model_name':       TaxCategory.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/taxes/categories',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return TaxCategory.Clayful.call_api({
			'model_name':       TaxCategory.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/taxes/categories/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return TaxCategory.Clayful.call_api({
			'model_name':       TaxCategory.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/taxes/categories/{taxCategoryId}',
			'params':           ('taxCategoryId', ),
			'args':             args
		})

