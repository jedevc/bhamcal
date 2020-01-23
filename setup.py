import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bhamcal',
    version='0.1',
    license='GPL 3',
    python_requires='>=3',

    author='Justin Chadwell',
    author_email='jedevc@gmail.com',

    url='https://github.com/jedevc/bhamcal',
    description='A timetable extractor for University of Birmingham',
    long_description=long_description,
    long_description_content_type='text/markdown',

    packages=setuptools.find_packages(),
    install_requires=[
        'click',
        'colorama',
        'beautifulsoup4',
        'pytz',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
    ],

    extras_require={
        'browser': ['selenium']
    },

    entry_points={
        'console_scripts': [
            'bhamcal=bhamcal:main'
        ]
    },
)
