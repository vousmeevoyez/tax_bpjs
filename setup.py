from setuptools import setup
from setuptools import find_packages

setup(name='tax_bpjs',
      version='1.0.4',
      description='Easy Tax & BPJS Calculation using Python!',
      url='https://github.com/vousmeevoyez/tax_bpjs',
      author='Kelvin Desman',
      author_email='kelvindsmn@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      install_requires=["python-dateutil"],
      python_requires='>=3')
