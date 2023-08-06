from setuptools import setup

setup(name='pyetherpix',
      version='0.3',
      description='python implementation of EtherPix output library',
      url='https://git.blinkenarea.org?p=pyetherpix',
      author='Stefan Schuermans',
      author_email='stefan@schuermans.info',
      license='LGPLv3',
      packages=['pyetherpix'],
      install_requires=['pillow'],
      zip_safe=False)

