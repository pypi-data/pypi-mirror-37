from setuptools import setup

setup(
    name='falcon_ask',
    version='1.1.0',
    description='Toolkit for writing Amazon Alexa skills in your Falcon app',
    author='Philamer Sune',
    author_email='pvsune@hotmail.com',
    url='https://github.com/pvsune/falcon_ask',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3.5',
        'Topic :: Home Automation',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    packages=['falcon_ask'],
    license='ISC',
    tests_require=['pytest'],
    install_requires=[
        'pyOpenssl==17.3.0'
    ]
)
