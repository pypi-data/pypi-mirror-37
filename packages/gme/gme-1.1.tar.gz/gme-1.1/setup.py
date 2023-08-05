from setuptools import setup, find_packages

setup(
    name='gme',
    version='1.1',
    description='USITC\'s Gravity Modeling Environment',
    long_description=open('README.txt').read(),
    keywords='gravity estimation ppml',
    url='https://gravity.usitc.gov',
    author='USITC Gravity Modeling Group',
    author_email='gravity@usitc.gov',
    license='',
    packages=find_packages(),
    install_requires=['pandas','statsmodels','scipy','patsy','pickle','numpy','typing','datetime','time','traceback'],
    zip_safe=False
)
