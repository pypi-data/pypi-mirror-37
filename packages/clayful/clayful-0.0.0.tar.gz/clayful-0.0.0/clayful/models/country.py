class Country:

	Clayful = None
	name = 'Country'
	path = 'countries'

	@staticmethod
	def config(clayful):

		Country.Clayful = clayful

		return Country

	@staticmethod
	def list(*args):

		return Country.Clayful.call_api({
			'model_name':       Country.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/countries',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Country.Clayful.call_api({
			'model_name':       Country.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/countries/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Country.Clayful.call_api({
			'model_name':       Country.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/countries/{countryId}',
			'params':           ('countryId', ),
			'args':             args
		})

