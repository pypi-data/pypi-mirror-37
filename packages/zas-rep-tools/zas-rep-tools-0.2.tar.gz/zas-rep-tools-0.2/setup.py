from setuptools import setup,find_packages

setup(name='zas-rep-tools',
      version='0.2',
      description='This Tool-set helps to make the repetition search in text much comfortable and faster.',
      url='https://github.com/savin-berlin/zas-rep-tools',
      git_url='https://github.com/savin-berlin/zas-rep-tools.git',
      author='Egor Savin',
      author_email='science@savin.berlin',
      license='MIT',
      #packages=find_packages('zas_rep_tools/'),
      packages=['zas_rep_tools_data','zas_rep_tools'],
      install_requires=[ 'sure','nose', 'rednose', 'blessings', 'testfixtures',
      'click', 'regex',  'cached_property', 'raven', "email",  "tweepy", "nltk",
      "langid",  "lxml", "logutils", "pyhashxx", "colored_traceback", "colorama",
      "unicodecsv","psutil","execnet","validate_email","console-menu","python-twitter", "twitter",
      "enlighten", "emoji", "textblob","textblob_de", "textblob_fr", "kitchen", "uniseg",
      "pystemmer", "ZODB"],
      include_package_data=True,    # include everything in source control
      zip_safe=False,
      test_suite='nose.collector', # test by installationls
      tests_require=['nose'], #test by installation
      entry_points={
          'console_scripts': [
              'zas-rep-tools=zas_rep_tools.cli.main:main',
          ],
      },
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
