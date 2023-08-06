# from distutils.core import setup

from setuptools import setup

def readme_file():
      with open('README.rst', encoding = 'utf-8') as rf:
          return rf.read()

setup(name='ljxtestlib', version='1.0.0', description='this is a niubi lix',
      packages=['ljxtestlib'], py_modules=['Tool'], author='Ljx', author_email='1169503322@qq.com',
      long_description=readme_file(),
      url='https://github.com/wangshunzi/Python_code',
      license='MIT')


