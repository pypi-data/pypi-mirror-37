from setuptools import setup,find_packages

setup(name='zas-rep-tools',
      version='0.1',
      description='This Tool-set helps to make a repetitions analysis in social media corpora much comfortable',
      url='https://github.com/savin-berlin/zas-rep-tools',
      git_url='https://github.com/savin-berlin/zas-rep-tools.git',
      author='Egor Savin',
      author_email='science@savin.berlin',
      license='MIT',
      #packages=find_packages('zas_rep_tools/'),
      packages=['zas_rep_tools'],
      install_requires=[ 'sure','nose', 'rednose', 'blessings', 'testfixtures',
      'click', 'regex',  'cached_propelsrty', 'raven', "email",  "tweepy", "nltk",
      "langid",  "lxml", "logutils", "pyhashxx", "colored_traceback", "colorama",
      "unicodecsv","psutil","execnet","validate_email","console-menu","python-twitter", "twitter",
      "enlighten", "emoji", "textblob","textblob_de", "textblob_fr", "kitchen", "uniseg",
      "pystemmer", "ZODB"],
      include_package_data=True,    # include everything in source control
      # package_data={
      #   # If any package contains *.txt or *.rst files, include them:
      #   '*': ['*',
      #   ],
      #   # And include any *.msg files found in the 'hello' package, too:
      #   'zas_rep_tools/': [
      #                     'tests/*.py',
      #                     'cli/*.py', 
      #                     'data/models/SoMeWeTa/*.model',
      #                     'data/models/stop_words/*.txt',

      #                     ],

      #   'zas_rep_tools/data/': ['*.*'],
      #   'zas_rep_tools/src': ['*.*'],
      #   'zas_rep_tools/*':['*'],
      # },
      #include_package_data=True,
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
      'Programming Language :: Python :: 2.7'
]
)
