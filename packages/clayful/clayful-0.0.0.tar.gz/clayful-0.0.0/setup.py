from setuptools import setup, find_packages

setup(
	name                          = 'clayful',
	version                       = '0.0.0',
	description                   = 'Python SDK for Clayful API',
	long_description              = open('README.md').read(),
	long_description_content_type = 'text/markdown',
	author                        = 'Daeik Kim',
	author_email                  = 'daeik.kim@clayful.io',
	url                           = 'https://github.com/Clayful/clayful-python',
	keywords                      = 'eCommerce clayful',
	license                       = 'MIT',
	packages                      = find_packages(),
	install_requires              = [
		'requests>2.1,<3'
	],
	extras_require   = {
		'test': ['httpretty>0.8']
	}
)