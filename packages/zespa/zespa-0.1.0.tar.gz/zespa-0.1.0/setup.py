from setuptools import setup

SHORT_DESCRIPTION = """
A tool to aggregate issues's story-point(estimate) by labels and time from ZenHub""".strip()

DEPENDENCIES = [
    'beautifultable',
    'fire',
    'requests',
    'tqdm',
]

TEST_DEPENDENCIES = [
]

VERSION = '0.1.0'
URL = 'https://github.com/showwin/ZenHub-SP-Aggregator'

setup(
    name='zespa',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    url=URL,

    author='showwin',
    author_email='showwin_kmc@yahoo.co.jp',
    license='Apache Software License',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    entry_points={
        'console_scripts': 'zespa = zespa.main:main'
    },

    keywords='ZenHub issue aggregate storypoint estimate',

    packages=['zespa'],

    install_requires=DEPENDENCIES,
    tests_require=TEST_DEPENDENCIES,
)
