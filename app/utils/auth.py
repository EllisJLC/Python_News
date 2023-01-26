from flask import session, redirect
from functools import wraps # functools = set of helper functions, 

# def login_required(func):
#   @wraps(func)
#   def wrapped_function(*args, **kwargs):
#     print('wrapper')
#     return func(*args, **kwargs)
  
#   return wrapped_function

# @login_required
# def callback():
#   print('hello')

# callback() # prints 'wrapper', then 'hello' 

def login_required(func):
  @wraps(func)
  def wrapped_function(*args, **kwargs):
    if session.get('loggedIn') == True:
      return func(*args, **kwargs)
    
    return redirect('/login')
  
  return wrapped_function