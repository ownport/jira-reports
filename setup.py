from setuptools import setup

from jirareports import __title__
from jirareports import __version__

setup(
    name=__title__,
    version=__version__,
    description='Jira reporting tools',
    url='https://github.com/ownport/jira-reports',
    author='ownport',
    author_email='ownport@gmail.com',
    py_modules=['jirareports'],
    packages=[
        'jirareports',
    ],
    entry_points={
        'console_scripts': [
            'jirareports = jirareports.main:run',
        ]
    },
    keywords=['jira', 'report', 'tool', 'dump'],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
)
