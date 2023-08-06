from setuptools import setup, find_packages

setup(
    name='shortesttrack-tools',
    version='0.1.7',
    packages=find_packages(),
    install_requires=[
        'URLObject==2.4.3',
        'requests==2.19.1',
        'requests-oauthlib==1.0.0',
        'pytz==2018.5',
        'PyJWT==1.6.1',
        'cryptography==2.2.1'
    ]
)
