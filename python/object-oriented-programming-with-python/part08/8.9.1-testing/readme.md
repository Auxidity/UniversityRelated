# Introduction to Python Testing with Pytest
Testing is a crucial part of software development that helps ensure your code behaves as expected. In Python, one of the most popular testing frameworks is pytest, known for its simplicity, scalability, and ability to handle both simple unit tests and complex functional testing.

## What is Pytest?
Pytest is a robust Python testing tool that simplifies the process of writing and running tests. It supports various types of tests including unit tests, integration tests, and end-to-end tests. Pytest is favored for its minimalistic approach where a small amount of boilerplate code is required to get started.

## Key Features of Pytest
- Simple to Use: Writing tests in pytest requires less code, making your tests cleaner and more readable.
- Fixtures: Reusable pieces of code that can be used to set up and tear down the state for tests.
- Parameterized Testing: Easily run a test function with different sets of arguments.
- Plugins: Extendable with a wide range of plugins for integration with other tools and frameworks.
- Rich Default Behaviors: Sensible defaults for most use cases.

## Getting Started with Pytest

### Installation
Pytest can be installed using pip:

```bash
pip install pytest
```

### Writing Your First Test
Pytest makes it easy to write tests. Here's a simple example:

```python
# test_example.py

def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
```

### Running Tests
To run your tests, simply execute the pytest command in your terminal:

```bash
pytest
```
Pytest will automatically discover and run any files named test_*.py or *_test.py.  

You can run the tests directly from vscode too, see  (https://code.visualstudio.com/docs/python/testing)

### Multiple file approach
In this folder you have the original ShoppingList class in one file `shopping.py`. This file contains class definitions only, no runnable code.   
Another file `test_shopping.py` contains the test cases for the class. In each test case, the code creates one object from the class, calls some methods to set the object in known state and tests one thing only (test case). You can run all test cases by just typing `pytest` in project terminal line.  

In designing the the test cases, you should consider creating
- a separate test case for each feature (method) in the class
- separate test case for all valid input combinations for constructor and methods
- separate test cases for invalid inputs (check for raised exceptions)

## To Do

You should now revisit previous exercises starting from 8.3.1-Book and 
- edit the original file to contain only necessary code (class definitions, possibly helper function methods)
- create a separate `test_[exercisename].py` file for each exercise, and insert necessary test cases for the class. Check the example in this folder again for reference.



