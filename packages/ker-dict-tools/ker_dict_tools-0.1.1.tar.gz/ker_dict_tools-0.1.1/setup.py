# from distutils.core import setup
import setuptools
# import os
# curr_dir = os.path.abspath(os.path.dirname(__file__))

with open('README.md') as f:
  long_description = f.read()


setuptools.setup(
  name = 'ker_dict_tools',         
  packages = ['ker_dict_tools'],   
  version = '0.1.1',      
  license='MIT',        
  description = 'Tools for smart operations with python dicts',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Luca Buccioni',                   
  author_email = 'kerkops7@gmail.com',      
  url = 'https://bitbucket.org/kerkops/dict_tools',  
  #download_url = 'https://bitbucket.org/kerkops/dict_tools/get/0.1.tar.gz',    
  keywords = [
    'dicts',
    'dict',
    'path',
    'paths',
    'paths for dicts',
    'dict diff',
    'dict differences',
    'diff',
    'operations on dictionaries',
    'dict values by path',
    'dict queries',
    'dict query',
    'differences between nested dicts',


    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   

    'Programming Language :: Python :: 3',
    
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
  ],
)