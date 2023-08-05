from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='netguru_recruitment_task_adrian',
      version='1.1',
      description='My implementation of Movies REST API',
      url='https://github.com/Qentinios/netguru_recruitment_task/commits/master',
      author='Adrian Czok',
      author_email='theadrianczok@gmail.com',
      license='MIT',
      packages=['movies_api'])
