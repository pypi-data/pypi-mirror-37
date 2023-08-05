from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

# with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(name='mowitnow',
      version='1.0',
      description='MowItNow Controller',
      long_description='Programme de controle d un ensemble de tondeuses.',
      url='https://github.com/xavbyme/mowitnow.git',
      keywords='mow mower tondeuse controle controller',
      author='XRU',
      author_email='ruiz.xvr@gmail.com',
      license='MIT',
      packages=['mowitnow'],
      install_requires=[
	'argparse'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
