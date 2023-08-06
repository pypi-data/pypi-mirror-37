from setuptools import setup


setup(
    name='scapinspector',
    version='1.0.5',
    packages=['scapinspector',],
    include_package_data=True,
    url='https://github.com/chris17453/scapinspector/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    summary= 'SCAP tool for parsing scap datastreams, creating tailoring files and parsing report results',
    author= 'Charles Watkins',
    author_email= 'charles@titandws.com',
    description= 'SCAP tool for parsing scap datastreams, creating tailoring files and parsing report results',
    platform= 'All',    
    install_requires=[
        'flask',
        'sqlalchemy',
        'pyyaml',
        'pymysql',
        'jsonpickle',
    ],

)



