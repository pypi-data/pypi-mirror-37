from setuptools import setup


setup(
    name='fio-py-Authorize',
    version='1.4.0.1',
    author='Vincent Catalano, Fulfil.IO Inc',
    author_email='info@fulfil.io',
    url='https://github.com/fulfilio/py-authorize',
    download_url='',
    description="A full-featured Python API for Authorize.net's AIM, CIM, ARB and Reporting APIs.",
    long_description=__doc__,
    license='MIT',
    install_requires=[
        'colander>=1.0b1',
    ],
    packages=[
        'authorize',
        'authorize.apis',
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
        'Topic :: Office/Business :: Financial',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
