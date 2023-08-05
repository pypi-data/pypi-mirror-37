from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ['requests', 'pyjwt']
requirements = ['unidecode', 'junitparser', 'pyyaml', 'click', 'requests', 'coloredlogs']
extra_requirements = {
    'dev': ['pytest>=3', 'coverage', 'pytest-cov', 'pytest-mock', ], 'docs': ['sphinx', ]
}
entry_points = dict(console_scripts=['ktdk = ktdk.cli:main_cli', ])
setup(name='ktdk',
      version='0.2',
      description='Kontr tests development kit',
      author='Peter Stanko',
      author_email='stanko@mail.muni.cz',
      url='https://gitlab.fi.muni.cz/grp-kontr2/ktdk',
      packages=find_packages(exclude=("tests",)),
      long_description=long_description,
      long_description_content_type='text/markdown',
      include_package_data=True,
      install_requires=requirements,
      extras_require=extra_requirements,
      entry_points=entry_points,
      classifiers=[
          "Programming Language :: Python :: 3",
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          "Operating System :: OS Independent",
          "License :: OSI Approved :: Apache Software License",
          'Intended Audience :: Developers',
          'Topic :: Utilities',
      ],)
