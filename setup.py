import os
from setuptools import setup, find_packages


def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(
    name = "usersService",
    version = "0.0.1",
    author = "Mariano Abdala",
    author_email = "marianoabdala@gmail.com",
    description = ("A mini architecture of a microservice API with users."),
    license = "BSD",
    packages=find_packages(),
    long_description=read('users/README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    data_files=[("users/README.md")],
    entry_points={
          'console_scripts': [
              'usersService = common.__main__:main'
          ]
      },
)