from setuptools import setup

setup(name='qtxpack',
      version='1.0',
      description='package to generate db connections',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['qtxpack'],
      install_requires=[
	'phoenixdb'
     ],
     zip_safe=False)
