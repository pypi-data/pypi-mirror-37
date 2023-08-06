from distutils.core import setup

setup(
    name='freshsales',
    version='1.0.0',
    author='Bhagirath Goud',
    author_email='bhagirath@freshdesk.com',
    packages=['freshsales'],
    url='http://pypi.python.org/pypi/Freshsales/',
    license='MIT',
    description='Freshsales integration.',
    long_description=open('README.txt').read(),
    install_requires=[
        "requests"
    ],
)
