from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='kfactor',
      version='0.1.0',
      description='k-Factor Nearest Correlation Matrix Fit',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/kmedian/kfactor',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['kfactor'],
      install_requires=[
          'setuptools>=40.0.0',
          'numpy>=1.14.5',
          'scipy>=1.1.0',
          'scikit-learn>=0.19.2'],
      python_requires='>=3.6',
      zip_safe=False)
