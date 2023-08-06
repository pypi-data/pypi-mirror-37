
# from distutils.core import setup
from setuptools import setup

def readme_file():
      with open("README.rst",encoding="utf-8") as rf:
            return rf.read()

setup(name="hxftestlib",version="1.1.6",description="this is a baqi lib2",
      packages=["hxftestlib"],py_modules=["Tool"],author="hxf",
      author_email="SO2@sina.com",long_description=readme_file(),url="https://github.com/SO2Family/Python_code",license="MIT")


