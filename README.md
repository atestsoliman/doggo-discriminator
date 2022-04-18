# Doggo Discriminator
A deliberately over-engineered tool for categorizing dogs and having fun with python.

## Setup
This is a personal project that has only been test on one machine. Please open an issue if these instructions don't work for you.
1. Clone the repo
2. Create an environment with `poetry install`
3. Try the sample app `dogs --help`
    - Follow the prompts!
    - Have fun!
4. Try the test suite with `pre-commit install` and `pre-commit run --all-files`
5. Look at the code.

## Structure
This project comprises 4 submodules and a test suite.

### Core
This module contains core classes used to manage the underlying logic of a labeling task.
Currently just some very basic data classes.

### Data Sinks
This module contains classes that manage sending data for storage.
Currently just a jsonlines serializer

### Data Sources
This module contains classes that manage receiving data to be labeled.
Currently just an api client that pull random images of dogs from the internet.

### Interfaces
This Module contains implementations of labeling interfaces that use the above modules.
Currently a CLI that prints dog images as ascii art, takes user input for whether the dog is a small doggo or a large pupper and stores the result in a jsonlines file.


## FAQ
Q: Is this a joke? <br>
A: Partly, the tools and techniques are real, the demo task is meant to be funny.


Q: Why are your tests in pre-commit hooks, and not CI isn't that bad practice? <br>
A: It can be especially with large test suites, but I wanted to force my commits to be coherent working chunks of code. Also see question 1.
