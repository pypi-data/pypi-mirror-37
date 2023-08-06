from setuptools import setup, find_packages

setup(
    name = 'cpbox',
    version = '0.0.12',
    keywords = ('cpbox'),
    description = 'cp tool box',
    license = '',
    install_requires = [
        'six>=1.11.0',
        'pyyaml>=3.12',
        'Jinja2>=2.9.6',
        'netaddr>=0.7.19',
        'requests>=2.18.4',
        'pytz>=3.6',
        'urllib3[secure]>=1.22',
        'cryptography>=2.2.1',
        'docker>=3.5.1',
        'redis>=2.10.6'
        ],

    scripts = [],

    author = 'http://www.liaohuqiu.net',
    author_email = 'liaohuqiu@gmail.com',
    url = '',

    packages = find_packages(),
    platforms = 'any',
)
