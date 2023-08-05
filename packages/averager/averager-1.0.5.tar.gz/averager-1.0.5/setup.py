import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='averager',
      version='1.0.5',
      description='A simple averager',
      url='http://github.com/bsoyka/averager',
      author='Benjamin Soyka',
      author_email='bensoyka@icloud.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=setuptools.find_packages(),
      license='GPL-3.0',
      zip_safe=False)
