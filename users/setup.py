from setuptools import setup, find_packages


setup(
    name = "usersService",
    version = "0.0.1",
    author = "Mariano Abdala",
    author_email = "marianoabdala@gmail.com",
    description = ("A mini architecture of a microservice API with users."),
    license = "BSD",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: API",
        "License :: Apache License",
    ],
    entry_points={
          'console_scripts': [
              'usersService = app:main'
          ]
      },
)
