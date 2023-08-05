from setuptools import setup

setup(name='hmtredishelp',
      version='0.1',
      description='A set of tools we use to easily access redis',
      url='https://github.com/IntuitionMachines/redis-tools',
      author='Intuition Machines',
      author_email='contact@intuitionmachines.com',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3'
      ],
      license='MIT',
      packages=['hmtredishelp'],
      install_requires=["redis"],
      zip_safe=False)
