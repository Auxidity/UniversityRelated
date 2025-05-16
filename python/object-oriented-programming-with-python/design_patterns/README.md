# Design patterns

Object-Oriented (OO) design patterns are fundamental concepts in software engineering, aimed at solving common design challenges in software development. These patterns provide templated solutions to problems that developers frequently encounter, making it easier to develop scalable, maintainable, and reusable code. The concept of design patterns in software development was popularized in the 1990s by the seminal book "Design Patterns: Elements of Reusable Object-Oriented Software" by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, collectively known as the "Gang of Four" (GoF).

OO design patterns are divided into three main categories:

1. Creational Patterns: These patterns deal with object creation mechanisms, trying to create objects in a manner suitable to the situation. The basic form of object creation could result in design problems or add complexity to the design. Creational patterns solve this problem by somehow controlling this object creation. Examples include the Singleton, Factory Method, Abstract Factory, Builder, and Prototype patterns.

2. Structural Patterns: These patterns concern class and object composition. They help ensure that if one part of a system changes, the entire system doesn't need to do the same. They help to create large, complex structures by using simple building blocks. Examples include the Adapter, Composite, Proxy, Flyweight, Facade, and Decorator patterns.

3. Behavioral Patterns: These patterns are all about class's objects communication. They help in defining how objects interact in a manner that increases flexibility in carrying out communication. Examples include the Observer, Command, Strategy, Iterator, Mediator, Memento, and State patterns.

Each pattern is a three-part rule that expresses a relationship between a certain context, a problem, and a solution. The context outlines when to use the pattern, the problem describes what needs to be addressed, and the solution offers a way to fulfill the objectives. It's important to note that these patterns are not finished designs that can be transformed directly into code; instead, they are guidelines or templates that can be adapted to solve a particular problem in an application's context.

Understanding and applying OO design patterns effectively can significantly improve the quality of software systems, making them more flexible, scalable, and maintainable. As such, knowledge of these patterns is considered essential for any proficient software developer.

## OO patterns in Python

Applying design patterns in Python, a dynamically typed language, differs from their implementation in statically typed languages like Java or C#. Python's flexibility and its support for multiple programming paradigms (procedural, object-oriented, and functional) mean that many of the constraints necessitating design patterns in other languages are not as applicable or can be addressed more straightforwardly. Before diving into how Python uses design patterns, let's clarify what interfaces and abstract classes are, as these concepts are central to understanding design patterns in more statically typed languages.

### Interfaces
An interface in programming defines a contract or a group of method signatures (methods without bodies) that a class agrees to implement. Interfaces dictate the methods a class should have, ensuring that irrespective of the specific type of the object, it can be used in a given context if it implements the interface. Java and C# are examples of languages that use interfaces explicitly.

### Abstract Classes
An abstract class is a class that cannot be instantiated on its own and is designed to be subclassed. It can contain both abstract methods (without an implementation) and concrete methods (with an implementation). The purpose of an abstract class is to provide a common definition of a base class that multiple derived classes can share. Abstract classes are used in languages like Java and C# to provide a template for future specific classes.

## Applying Design Patterns in Python
In Python, the explicit declaration of interfaces and abstract classes is not required due to its dynamic nature. However, concepts similar to interfaces and abstract classes can still be used with the help of modules like abc (Abstract Base Classes) to enforce the implementation of methods in subclasses.

### Abstract Base Classes
Python's abc module enables the use of abstract base classes, which can define a set of methods that must be created within any child classes built from the abstract base class. This is similar to abstract classes in other languages but is not as strictly required because Python uses duck typing (if it looks like a duck and quacks like a duck, it must be a duck).

```python
from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    @abstractmethod
    def get(self, item_id):
        pass

    @abstractmethod
    def save(self, item):
        pass
```

### Interfaces
While Python does not have a formal mechanism for interfaces, the concept is implicitly supported through duck typing. A class in Python is considered to implement an interface simply by providing implementations for the methods that the interface requires. The zope.interface package can also be used for a more formal approach to interfaces.

### Applying Design Patterns
When applying design patterns in Python:

1. Creational Patterns: Python's dynamic nature simplifies object creation. For example, the Factory Method pattern, which involves an interface for creating objects but allows subclasses to alter the type of objects that will be created, can be implemented more succinctly without needing explicit class-based factories.

2. Structural Patterns: Adapter pattern implementations are more straightforward because Python can add or modify class methods at runtime. Decorators in Python also directly support the Decorator pattern, allowing for the dynamic wrapping of objects.

3. Behavioral Patterns: The Strategy pattern, which defines a family of algorithms, encapsulates each one, and makes them interchangeable, is easily implemented in Python by simply passing different functions as arguments to methods or using callables.

Python's dynamic typing and its support for first-class functions and closures mean that many design patterns can be implemented more succinctly and with less boilerplate than in statically typed languages. The language's features encourage a different approach to solving the problems that design patterns aim to address, often leading to more Pythonic solutions that leverage the language's strengths.

## To do

The topic of design patterns is quite extensive. In this course there are two design pattern examples with some refactoring tasks to do. You find those in subfolders here.








