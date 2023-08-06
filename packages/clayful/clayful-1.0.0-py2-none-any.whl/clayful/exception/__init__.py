class ClayfulException(Exception):

	def __init__(
		self,
		model = None,
		method = None,
		status = None,
		headers = None,
		code = None,
		message = '',
		validation = None):

		self.is_clayful = True
		self.model = model
		self.method = method
		self.status = status
		self.headers = headers
		self.code = code
		self.message = message
		self.validation = validation

		super(ClayfulException, self).__init__(message)