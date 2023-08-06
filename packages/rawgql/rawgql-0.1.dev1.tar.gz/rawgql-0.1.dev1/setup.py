from setuptools import setup

with open('README.md', 'r') as f:
    ld = f.read()

setup(name='rawgql',
      version='0.1.dev1',
      description='Simple Python 3 framework for interacting with GraphQL endpoints',
      long_description=ld,
      long_description_content_type='text/markdown',
      url='https://github.com/jamwil/rawgql',
      author='James Williams',
      author_email='jamwil@gmail.com',
      py_modules=['rawgql'],
      license='MIT',
      keywords=('graphql'),
      install_requires=[
          'requests'
      ],
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Development Status :: 3 - Alpha',
          'Natural Language :: English',
          'Topic :: Database'
      ])
