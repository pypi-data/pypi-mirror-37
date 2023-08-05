from setuptools import find_packages
from setuptools import setup


try:
    README = open('README.rst').read()
except IOError:
    README = None

setup(
    name='guillotina_amqp',
    version='1.0.7',
    description='Integrate amqp into guillotina',
    long_description=README,
    install_requires=[
        'guillotina>=2.1.5',
        'aioamqp',
        'lru-dict'
    ],
    author='Nathan Van Gheem',
    author_email='vangheem@gmail.com',
    url='https://github.com/guillotinaweb/guillotina_amqp',
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    tests_require=[
        'pytest'
    ],
    extras_require={
        'test': [
            'pytest<=3.1.0',
            'docker',
            'backoff',
            'psycopg2',
            'pytest-asyncio>=0.8.0',
            'pytest-aiohttp',
            'pytest-cov',
            'coverage==4.0.3'
        ]
    },
    license='BSD',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
    ],
    entry_points={
    }
)
