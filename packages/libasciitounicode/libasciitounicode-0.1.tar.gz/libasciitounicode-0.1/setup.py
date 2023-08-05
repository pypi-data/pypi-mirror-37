from setuptools import setup, find_packages

setup(name='libasciitounicode',
      version='0.1',
      url='https://github.com/akuru/libasciitounicode',
      license='MIT',
      author='Keshan Sodimana',
      author_email='keshan88@gmail.com',
      description='Library to convert ASCII encodings to unicode',
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'PyYAML',
      ],
      long_description=open('README.md').read(),
      zip_safe=False)
