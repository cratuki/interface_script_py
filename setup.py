from distutils.core import setup

NAME = 'interface_script'
VERSION = '1.1'

setup(
  name = NAME,
  packages = [NAME],
  version = VERSION,
  license='MIT',
  description = 'Message-oriented data-interchange format',
  author = 'Craig Turner',
  author_email = 'cratuki@gmail.com',
  url = 'https://github.com/cratuki/interface_script_py',
  download_url = 'https://github.com/cratuki/interface_script_py/archive/v%s.tar.gz'%(VERSION),
  keywords = ['interchange', 'textual', 'message-driven', 'event-driven'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
