from setuptools import setup

setup(name='maltego-trx',
      version='1.2',
      description='Python library used to develop Maltego transforms',
      url='https://github.com/paterva/maltego-trx/',
      author='Paterva Staff',
      author_email='technical@paterva.com',
      license='MIT',
      install_requires=[
       'flask>=1',
       'six>=1'
      ],
      packages=[
          'maltego_trx',
          'maltego_trx/template_dir',
          'maltego_trx/template_dir/transforms'
      ],
      entry_points={'console_scripts': [
          'maltego-trx = maltego_trx.commands:execute_from_command_line',
      ]},
      zip_safe=False
      )
