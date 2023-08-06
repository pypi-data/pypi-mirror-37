from setuptools import setup, find_packages

# loading __version__
exec(open('pylintconfig/version.py').read())

with open('readme.md', 'r') as f:
    readme = f.read()

setup(
    name='pylintconfig',
    version=__version__,
    packages=find_packages(),
    description='cli for easy configuration of pylint',
    url='https://github.com/GliderGeek/pylintconfig',
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'Click',
        'pylint',
    ],
    entry_points='''
        [console_scripts]
        pylintconfig=pylintconfig.pylintconfig:pylintconfig
    ''',
)
