from setuptools import setup

setup(name='pygeek-stellar',
      version='0.2',
      description='A Python CLI to interact with the Stellar network.',
      url='https://github.com/XavierAraujo/pygeek-stellar',
      author='Xavier Araújo',
      author_email='xavier.araujo92@gmail.com',
      license='MIT',
      packages=['pygeek_stellar', 'pygeek_stellar.utils'],
      install_requires=[
            'stellar-base',
            'cryptography',
            'requests'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/pygeek-stellar'],
      python_requires='>=3.7',
      zip_safe=False)
