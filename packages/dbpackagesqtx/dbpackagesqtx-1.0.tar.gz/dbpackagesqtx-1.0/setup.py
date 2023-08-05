from setuptools import setup

setup(name='dbpackagesqtx',
      version='1.0',
      description='database connection strings',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['dbpackagesqtx'],
      install_requires=[
	'phoenixdb'
     ],
     zip_safe=False)
