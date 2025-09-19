# 1.Object and classes
class Person:
    pass


p = Person()  # we are creating instance object of class object Person
p.__class__  # this will be give you class object


# class attributes
class Program:
    language = 'Python'
    version = '3.10'


p = Program()
Program.__name__  # instance object "p" does not have attribute __name__

# Notice also that Program.__dict__ does not return a dictionary, but a mappingproxy object - this is essentially a read-only dictionary that we cannot modify directly (but we can modify it by using setattr, or dotted notation).
getattr(Program, "version")  # Program.__dict__['version]
# Program.__dict__['latest_version']='3.13'
setattr(Program, 'latest_version', '3.13')
delattr(Program, 'y')  # del Program.__dict__['y']
list(Program.__dict__.items())

# One word of caution: not every attribute that a class has lives in that dictionary (we'll come back to this later).


#############################
# Callable class attributes
###########################
class Program:
    language = 'Python'

    def say_hello():
        print(f'Hello from {Program.language}!')


Program.say_hello, getattr(Program, 'say_hello')
Program.__dict__['say_hello']()


#####################
# Classes are Callable
####################

# As we saw earlier, one of the things Python does for us when we create a class is to make it callable.

# Calling a class creates a new instance of the class - an object of that particular type.

class Program:
    language = 'Python'

    def say_hello():
        print(f'Hello from {Program.language}!')


p = Program()
isinstance(p, Program)
# These instances have their own namespace, and their own __dict__ that is distinct from the class __dict__:


class MyClass:
    __class__ = str


m = MyClass()
type(m), m.__class__


class BankAccount:
    apr = 1.2
