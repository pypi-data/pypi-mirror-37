class Group:

	Clayful = None
	name = 'Group'
	path = 'groups'

	@staticmethod
	def config(clayful):

		Group.Clayful = clayful

		return Group

	@staticmethod
	def list(*args):

		return Group.Clayful.call_api({
			'model_name':       Group.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/groups',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Group.Clayful.call_api({
			'model_name':       Group.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/groups/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Group.Clayful.call_api({
			'model_name':       Group.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/groups/{groupId}',
			'params':           ('groupId', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Group.Clayful.call_api({
			'model_name':       Group.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/groups/{groupId}/meta/{field}/inc',
			'params':           ('groupId', 'field', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Group.Clayful.call_api({
			'model_name':       Group.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/groups/{groupId}/meta/{field}/pull',
			'params':           ('groupId', 'field', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Group.Clayful.call_api({
			'model_name':       Group.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/groups/{groupId}/meta/{field}/push',
			'params':           ('groupId', 'field', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Group.Clayful.call_api({
			'model_name':       Group.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/groups/{groupId}/meta/{field}',
			'params':           ('groupId', 'field', ),
			'args':             args
		})

