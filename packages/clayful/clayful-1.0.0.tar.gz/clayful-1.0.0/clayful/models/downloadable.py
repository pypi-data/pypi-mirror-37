class Downloadable:

	Clayful = None
	name = 'Downloadable'
	path = 'downloadables'

	@staticmethod
	def config(clayful):

		Downloadable.Clayful = clayful

		return Downloadable

	@staticmethod
	def list(*args):

		return Downloadable.Clayful.call_api({
			'model_name':       Downloadable.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/downloadables',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Downloadable.Clayful.call_api({
			'model_name':       Downloadable.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/downloadables/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Downloadable.Clayful.call_api({
			'model_name':       Downloadable.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/downloadables/{downloadableId}',
			'params':           ('downloadableId', ),
			'args':             args
		})

	@staticmethod
	def create_download_url(*args):

		return Downloadable.Clayful.call_api({
			'model_name':       Downloadable.name,
			'method_name':      'create_download_url',
			'http_method':      'POST',
			'path':             '/v1/downloadables/{downloadableId}/url',
			'params':           ('downloadableId', ),
			'without_payload':  True,
			'args':             args
		})

