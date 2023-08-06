from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='threesplit',
      version='0.1.0',
      description=(
          "Three-way data split into training set, "
          "validation set, and test set."),
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/kmedian/threesplit',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['threesplit'],
      install_requires=[
          'setuptools>=40.0.0',
          'numpy>=1.14.5'],
      python_requires='>=3.6',
      zip_safe=False)
