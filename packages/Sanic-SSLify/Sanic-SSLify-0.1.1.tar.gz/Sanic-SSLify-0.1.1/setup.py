"""
Sanic-SSLify
------------
This is a simple Sanic extension that configures your Sanic application to redirect
all incoming requests to ``https``.
Redirects only occur when ``app.debug`` is ``False``.
"""

from setuptools import setup

setup(
    name='Sanic-SSLify',
    version='0.1.1',
    url='https://github.com/dzqdzq/Sanic-sslify',
    license='MIT',
    author='dzqdzq',
    author_email='1246747572@qq.com',
    description='Force SSL on your Sanic app.',
    long_description=__doc__,
    py_modules=['sanic_sslify'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['sanic'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)