from distutils.core import setup
setup(
  name = 'dreambox',
  packages = ['dreambox'], 
  version = '0.9.4',
  description = 'Dreambox lib, tested with dm-800HD se',
  author = 'Damiano Pertolunio',
  author_email = 'github.5f16ec@tryninja.io',
  url = 'https://github.com/eneasz/dreambox', 
  download_url = 'https://github.com/eneasz//dreambox/archive/0.9.4.tar.gz',
  keywords = ['Dreambox', 'DM800 HD', 'DM800 HD se', 'Dream', 'Multimedia'], 
  classifiers = [],
  long_description = open('README.md').read(),
  install_requires=['lxml']
)
