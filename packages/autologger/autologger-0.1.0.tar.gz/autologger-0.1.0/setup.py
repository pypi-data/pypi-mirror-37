from setuptools import setup, find_packages

setup(
    name='autologger',
    version='0.1.0',
    url='https://github.com/matthewh/autologger',
    license='COMPANY-PROPRIETARY',
    maintainer='Matthew Hershberger',
    maintainer_email='matthewh@multipart.net',
    description='Automatically configure logging',
    long_description='Automatically configure logging',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'colorlog',
        'structlog'
    ]
)
