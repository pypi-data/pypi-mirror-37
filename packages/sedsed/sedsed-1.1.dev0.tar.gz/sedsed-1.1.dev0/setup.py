from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='sedsed',
      version='1.1-dev',
      description='Debugger, indenter and HTMLizer for sed scripts',
      url='http://github.com/aureliojargas/sedsed',
      author='Aurelio Jargas',
      license='MIT License',
      packages=['sedsed'],
      scripts=['sedsed/scripts/sedsed'],
      tests_require=['pytest'],
      zip_safe=True,
      include_package_data=True
)

