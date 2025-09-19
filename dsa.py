# fibonacci series
# 1
from functools import wraps


def fib1(n):
    if n <= 1:
        return n
    return fib1(n-1)+fib1(n-2)


# 2 with memorization
memo2 = [None]*10000


def fib2(n):
    if memo2[n] is not None:
        return memo2[n]
    if n <= 1:
        return n
    return fib2(n-1)+fib2(n-2)

# 2 computation efficirent


def fib3(n):
    a, b = 0, 1
    l1 = []
    for _ in range(n):
        l1.append(a)
        a, b = b, a+b
    return l1

# 3 generator


def fib4(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a+b


def fib_fast_doubling(n):
    """Return (F(n), F(n+1)) using fast doubling method"""
    if n == 0:
        return (0, 1)
    a, b = fib_fast_doubling(n // 2)
    c = a * (2*b - a)         # F(2k)
    d = a*a + b*b             # F(2k+1)
    if n % 2 == 0:
        return (c, d)
    else:
        return (d, c + d)


def my_decorator(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):   # Accept all positional and keyword args
        print(f"Before calling {fn.__name__}")
        print(f"Positional args: {args}")
        print(f"Keyword args: {kwargs}")
        # Forward them unpacked to the original function
        result = fn(*args, **kwargs)
        print(f"After calling {fn.__name__}")
        return result
    return wrapper


@my_decorator
def example_func(a, b=2, *args, c=3, **kwargs):
    print(f"a={a}, b={b}, args={args}, c={c}, kwargs={kwargs}")


# Call with various args:
example_func(1, 5, 7, 8, c=10, d=11, e=12)

# sort the dictionary based on values
d1 = {'a': 3, 'b': 4, 'c': 2, 'd': 1, 'e': 5, 'f': 1, 'g': 2}
d2 = sorted(d1.items(), key=lambda x: x[1])
