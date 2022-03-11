from setuptools import setup, find_packages


setup(
    name='Bel_messenger_server',
    version='0.1.0',
    description='Bel_messenger. Server_app',
    author='Sergey Sukhanov',
    author_email='sergey.bv26@gmail.com',
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
    scripts=['server/server_run']
)
