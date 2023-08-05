"""Installation setup
"""

from setuptools import setup

SPARKMANAGER_NAME = 'sparkmanager'


setup(
    name=SPARKMANAGER_NAME,
    description='A pyspark management framework',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    use_scm_version=True,
    author='Matthias Wolf',
    author_email='matthias.wolf@epfl.ch',
    license='MIT',
    keywords=['apache-spark'],
    url='https://github.com/matz-e/sparkmanager',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
    packages=[
        'sparkmanager',
    ],
    install_requires=[
        'pyspark',
        'six'
    ],
    setup_requires=[
        'pytest-runner',
        'setuptools-scm',
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    scripts=[
        'scripts/sm_cluster',
        'scripts/sm_run',
        'scripts/sm_startup',
        'scripts/sm_shutdown',
    ]
)
