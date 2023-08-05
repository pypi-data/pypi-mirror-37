from setuptools import setup

setup(name='arcticrepository',
      version='0.9',
      description='Wrapper of the Arctic library that includes ElasticSearch indexing',
      url='',
      author='Tim Watson, Jamie Wooltorton, Henry Jolliffe, Ryszard Dudek, Clare Ford',
      author_email='tswatson123@gmail.com',
      license='MIT',
      install_requires=[
        "arctic==1.68.0",
        "pandas== 0.23.4",
        "requests"
      ],
      packages=['arcticrepository'])
