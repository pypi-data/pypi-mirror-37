from setuptools import setup, find_packages

setup(
    name = 'cpbox',
    version = '0.0.1',
    keywords = ('cpbox'),
    description = 'cp tool box',
    license = '',
    install_requires = [
        'pyyaml',
        'Jinja2',
        'netaddr',
        'requests',
        'pytz',
        'urllib3[secure]',
        'cryptography>=2.2.1',
        'redis'
        ],

    scripts = [],

    author = 'http://www.liaohuqiu.net',
    author_email = 'liaohuqiu@gmail.com',
    url = '',

    packages = find_packages(),
    platforms = 'any',
)
