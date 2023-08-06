"""
hrf_opt setup.

For development installation:
    pip install -e /path/to/hrf_opt
"""

from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(name='hrf_opt',
      version='1.0.1',
      description=('Optimize hemodynamic response function parameters.'),
      url='https://github.com/MSchnei/hrf_opt',
      author='Marian Schneider',
      author_email='marian.schneider@maastrichtuniversity.nl',
      license='GNU General Public License Version 3',
      install_requires=['numpy', 'scipy', 'nibabel', 'cython==0.27.1',
                        'scikit-learn==0.19.1', 'pyprf_feature==1.1.0'],
      keywords=['pRF', 'fMRI', 'retinotopy'],
      long_description=long_description,
      packages=['hrf_opt'],
      entry_points={
          'console_scripts': [
              'hrf_opt = hrf_opt.__main__:main',
              ]},
      )
