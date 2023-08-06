"""
A setuptools-based setup module.

See:
https://github.com/YendiyarovSV/kafka-metrics-producer-topkrabbensteam
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
if path.exists(path.join(here, 'README.md')):
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = ''

setup(
    name='kafka-metrics-producer-topkrabbensteam',
    version='1.0',

    description='Library that can be used to produce metrics to Kafka using Apache Avro schemas',
    long_description=long_description,
    url='https://github.com/YendiyarovSV/kafka-metrics-producer-topkrabbensteam',
    author='Sergei Yendiyarov',
    author_email='s.endiyarov@gmail.com',
    license='License :: OSI Approved :: Apache Software License',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='kafka avro metrics prometheus producer',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=[]),
    package_data={'': ['README.md']},
    install_requires=['six==1.11.0',
                      'avro_gen_topkrabbensteam>=0.0.2',
                      'kafka-avro-producer-topkrabbensteam>=1.2'],
)

