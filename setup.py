from setuptools import setup

setup(name='passbook',
      version='0.1',
      description='Telegram Bot used to store encripted passwords',
      url='https://github.com/asierzapata/PassBook',
      author='Asier Zapata',
      author_email='asier.zapata@gmail.com',
      license='MIT',
      packages=['passbook'],
      install_requires=[
          'python-telegram-bot',
          'pymongo',
          'pycrypto'
      ],
      #data_files=[('', ['passbook/settings.json'])],
      package_data={'passbook':['settings.json']},
      include_package_data=True,
      zip_safe=False)
