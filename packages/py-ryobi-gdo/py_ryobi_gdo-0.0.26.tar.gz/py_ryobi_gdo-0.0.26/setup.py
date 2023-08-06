from setuptools import setup


setup(
    name='py_ryobi_gdo',
    version='0.0.26',
    description='Python package for controlling Ryobi Garage Door',
    author='Guillaume1410',
    author_email='super.guillaume@gmail.com',
    url='https://github.com/guillaume1410/py_ryobi_gdo',
    license='MIT',
    packages=['py_ryobi_gdo'],
    install_requires = ['websocket-client==0.37.0'],
    package_dir={'py_ryobi_gdo': 'py_ryobi_gdo'}
)
