# setup file in order to create a python applicaiton pacakge using setuptools
from setuptools import setup, find_packages

setup(
    # module name
    name='pyolos',
    version='0.5',
    description='Command line interface supporting CRUD operations to make deposits on the OLOS.swiss preservation infrastructure.',
    licence='MIT',
    author='Frédéric Noyer',
    author_email='frederic.noyer@plateforme10.ch',
    py_modules=['pyolosCLI'],
    install_requires=[
        'Click==8.0.3',
        'Configparser==5.2.0',
        'python-dotenv==0.19.2',
        'requests==2.26.0',
        'datetime==4.3',
        'Jinja2==3.0.3',
        'pytest==6.2.5',
        'python-benedict==0.24.3'
    ],
    entry_points='''
        [console_scripts]
        pyolos=pyolosCLI:cli
    ''',
    package=find_packages('pyolos'),
    package_dir={'': 'pyolos'},
    package_data={'': ['pyolos/conf/*.ini','pyolos/test_data/ISS_March_2009_NASA_CC0.jpg', 'pyolos/test_data/dlcm.xml']}
)
