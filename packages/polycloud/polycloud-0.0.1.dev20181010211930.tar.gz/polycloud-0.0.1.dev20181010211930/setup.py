
from setuptools import setup, find_packages
from polycloud.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='polycloud',
    version=VERSION,
    description='Manage your open polycloud platform.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Dennis Seidel',
    author_email='denseidel@gmail.com',
    url='https://github.com/denseidel/platform/tree/master/cli',
    license='MIT',
    install_requires=[
        'cement',
        'jinja2',
        'pyyaml',
        'colorlog',
    ], 
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'polycloud': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        polycloud = polycloud.main:main
    """,
)
