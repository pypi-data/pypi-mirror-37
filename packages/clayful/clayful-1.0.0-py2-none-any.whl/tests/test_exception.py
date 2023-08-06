import unittest
from clayful.exception import ClayfulException

class ClayfulExceptionTest(unittest.TestCase):

	def test_clayful_error_constructor(self):

		error = ClayfulException(
			'Brand',
			'get',
			400,
			{},
			'g-no-model',
			'my message',
			{}
		)

		self.assertEqual(error.is_clayful, True)
		self.assertEqual(error.model, 'Brand')
		self.assertEqual(error.method, 'get')
		self.assertEqual(error.status, 400)
		self.assertEqual(error.headers, {})
		self.assertEqual(error.code, 'g-no-model')
		self.assertEqual(error.message, 'my message')
		self.assertEqual(error.validation, {})

	def test_throw_clayful_error(self):

		try:

			raise ClayfulException(
				'Brand',
				'get',
				400,
				{},
				'g-no-model',
				'my message',
				{}
			)

		except ClayfulException as e:

			self.assertEqual(e.is_clayful, True)