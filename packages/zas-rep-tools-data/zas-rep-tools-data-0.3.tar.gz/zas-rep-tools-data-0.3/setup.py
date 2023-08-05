from setuptools import setup,find_packages

setup(name='zas-rep-tools-data',
      version='0.3',
      description='This is the data-set for "zas-rep-tools" package.',
      url='https://github.com/savin-berlin/zas-rep-tools-data',
      git_url='https://github.com/savin-berlin/zas-rep-tools-data.git',
      author='Egor Savin',
      author_email='science@savin.berlin',
      license='MIT',
      #packages=find_packages('zas_rep_tools/'),
      packages=['zas_rep_tools_data'],
      install_requires=[],
      include_package_data=True,    # include everything in source control
      zip_safe=False,
      test_suite='nose.collector', # test by installationls
      tests_require=['nose'], #test by installation
      classifiers=[ 
          'Development Status :: 1 - Planning', 
          'Intended Audience :: Science/Research', 
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows :: Windows 10",
          "Operating System :: Unix",
          "Programming Language :: Java",
          "Programming Language :: Python :: 3",
          "Topic :: Scientific/Engineering :: Information Analysis",
          "Topic :: Text Processing :: Linguistic",
                    ]
)
