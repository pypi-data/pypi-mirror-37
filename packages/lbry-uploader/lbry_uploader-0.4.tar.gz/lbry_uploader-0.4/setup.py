from setuptools import setup

setup(name='lbry_uploader',
      version='0.4',
      description='A simple uploader tool for LBRY',
      url='https://github.com/marcdeb1/lbry-uploader',
      author='marcdeb',
      author_email='marcdebrouchev@laposte.net',
      license='MIT',
      packages=['lbry_uploader'],
      install_requires=['pybry', 'pandas', 'tinydb', 'click', 'slugify'],
      zip_safe=False)