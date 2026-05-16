# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# @my_decorator
# def say_hello():
#     print("Hello!")

# say_hello()
# A simple registry system
# PLUGINS = {}

# def register(func):
#     PLUGINS[func.__name__] = func  # Save the function to our registry
#     return func                    # Return the original function directly

# @register
# def say_hello():
#     return "Hello!"

# # The function works normally, but is now tracked
# print(say_hello)  # Output: {'say_hello': <function say_hello at ...>}


# x = 'global'
# def outer():
#     x = 'enclosing'
# def inner():
#     x = 'local'
# outer()
# print(outer()) # 'local'

class X: pass
class Y(X): pass
class Z(X): pass
class W(Y, Z): pass
print(W.mro())
