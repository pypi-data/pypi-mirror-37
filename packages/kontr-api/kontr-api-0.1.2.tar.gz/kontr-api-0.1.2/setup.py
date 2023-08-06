from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ['requests', 'pyjwt']

extra_requirements = {
          'dev': [
              'pytest',
              'coverage',
              'mock',
              ],
          'docs': ['sphinx']
          }


setup(name='kontr-api',
      version='0.1.2',
      description='Kontr Portal REST Api Client',
      author='Peter Stanko',
      author_email='stanko@mail.muni.cz',
      maintainer='Peter Stanko',
      url='https://gitlab.fi.muni.cz/grp-kontr2/kontr-api',
      packages=find_packages(exclude=("tests",)),
      long_description=long_description,
      long_description_content_type='text/markdown',
      include_package_data=True,
      install_requires=requirements,
      extras_require=extra_requirements,
      entry_points={},
      classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        ],
      )
