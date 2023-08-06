from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='oxyba',
      version='0.30.0',
      description='my wrapper functions and classes for python',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/ulf1/oxyba',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['oxyba'],
      install_requires=[
          'numpy', 'scipy', 'matplotlib', 'urllib3',
          'setuptools', 'datetime', 'nose',
          'onepara', 'grouplabelencode', 'luriegold', 'kfactor',
          'illmat', 'randdate'],
      python_requires='>=3',
      zip_safe=False)
