from setuptools import setup

with open("Readme.rst", "r") as fh:
      long_description = fh.read()

setup(name='justify',
      version='0.3',
      description='An art of writing json',
      author='Akash Chaudhari',
      author_email='chaudharia041@gmail.com',
      license='MIT',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      packages=['json_justify'],
      zip_safe=False,
      url="https://github.com/AngrySoilder/json-justify",
      install_requires=['email_validator'],
      classifiers = [
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.5",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      ]
      )
