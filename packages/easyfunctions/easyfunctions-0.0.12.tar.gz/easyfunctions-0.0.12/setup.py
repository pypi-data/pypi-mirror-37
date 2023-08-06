from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='easyfunctions',
      version='0.0.12',
      description='Package of helper objects that contain methods to process datasets and variables for data mining and statistical modeling',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://gitlab.easytaxi.net.br/ops/gba/easy-analytics-dev-functions',
      author='Data & Analytics Team @MaxiMobility Bogota',
      author_email='jose.casas@easytaxi.com.co',
      license='',
      packages=['easyfunctions'],
      install_requires=[
          'pandas',
          'numpy'
      ],
      zip_safe=False
     )
