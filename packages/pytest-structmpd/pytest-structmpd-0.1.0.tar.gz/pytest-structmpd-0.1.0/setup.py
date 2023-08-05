from setuptools import setup


setup(
    name='pytest-structmpd',
    version='0.1.0',
    description='provide structured temporary directory',
    author='Daisuke Tanaka',
    author_email='duaipp@gmail.com',
    url='https://github.com/disktnk/pytest-structmpd',
    packages=['structmpd'],
    entry_point={'pytest11': ['structmpd = structmpd.plugin']},
    install_requires=[
        'pytest',
    ],
    test_require=[],
)
