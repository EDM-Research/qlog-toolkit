from setuptools import setup

setup(name='qlog_toolkit',
      version='0.1',
      description='a toolkit for qlog files',
      url='https://github.com/EDM-Research/qlog-toolkit',
      author='Mike Vandersanden',
      author_email='mike.vandersanden@uhasselt.be',
      license='MIT',
      packages=['qlogtk'],
      scripts=["bin/qlogtk"],
      )
