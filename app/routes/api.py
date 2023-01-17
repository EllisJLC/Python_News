from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys # Access interpreter functions

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json() # Grabs request info
  db = get_db()
  try: 
    newUser = User( # Creates new user based on request information.
      username = data['username'], # reference items in an object by using object['key']
      email = data['email'],
      password = data['password']
    )
    db.add(newUser) # Stage the new user to commit.
    db.commit()
  
  except: 
    print(sys.exc_info()[0]) # System execution error info
    db.rollback() # Rollback and send error if insert fails
    return jsonify(message='Signup failed, try again.'),500 # Input message, then error code

  session.clear()
  session['user_id'] = newUser.id # Set session user id
  session['loggedIn'] = True # Save session loggedIn object as True

  return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  try:
    print(session['user_id'])
    session.clear() # Clear logged in session
    return '', 204 # Return success, no content
  except:
    return 'logout error',400

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()
  try: 
    user = db.query(User).filter(User.email == data['email'].one())
  except:
    print(sys.exc_info()[0])
    return jsonify(message = "Login failed. Please try again."),400
  if user.verify_password(data['password']) == False:
    return jsonify(message = "Login failed. Please try again."),400
  
  session.clear()
  session['User'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)