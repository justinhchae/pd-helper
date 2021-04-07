from distutils.core import setup
setup(
  name = 'pd_helper',
  packages = ['pd_helper'],
  version = '0.0.1',
  license='MIT',
  description = 'A helpful script to optimize a Pandas DataFrame.',
  author = 'Justin Chae',
  author_email = 'justin@chaemail.com',
  url = 'https://github.com/justinhchae/pd-helper',
  download_url = 'https://github.com/justinhchae/pd-helper/archive/refs/tags/v0.0.1-beta.tar.gz',  
  keywords = ['pandas', 'dataframe', 'optimization'],
  install_requires=[
          'pandas',
          'numpy',
          'logging',
          'multiprocessing',
          'tqdm',
          'functools'
                   ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8',
  ],
)