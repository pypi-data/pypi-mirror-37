from distutils.core import setup
import platform

install_requires = []

if platform.system() == 'Windows':
    install_requires.append('mecab-python-windows')
else:
    install_requires.append('mecab-python3')


setup(name='MeCabOnigiri',
      version='0.2.1',
      description='Python Distribution Utilities',
      author='uehara1414',
      author_email='akiya.noface@gmail.com',
      url='https://github.com/uehara1414/MeCabOnigiri',
      packages=['MeCabOnigiri'],
      install_requires=install_requires,
      )
