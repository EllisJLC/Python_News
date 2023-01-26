from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys # Access interpreter functions
from app.utils.auth import login_required

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
  session.clear() # Clear logged in session
  return '', 204 # Return success, no content

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()
  try: 
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])
    return jsonify(message = "Login failed. Please try again."),400
  if user.verify_password(data['password']) == False:
    return jsonify(message = "Login failed. Please try again."),400
  
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)

@bp.route('/comments', methods=['POST'])
@login_required
def comment():
  data = request.get_json()
  db = get_db()
  try: 
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )
    
    db.add(newComment)
    db.commit()
  
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Comment could not be submitted, please try again.'), 500

  return jsonify(id = newComment.id)

@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
  data = request.get_json()
  db = get_db()
  print(data['post_id'])
  print(session.get('user_id'))
  try: 
    newVote = Vote( # Create a new vote item
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )
    print(newVote)

    db.add(newVote) # Stage
    db.commit() # Commit
  
  except:
    print(sys.exc_info()[0]) # Print error

    db.rollback() # Rollback commit

    return jsonify(message = "Cannot upvote, please try again."), 500

  return '', 204

@bp.route('/posts', methods = ['POST']) # Create post route
@login_required
def create():
  data = request.get_json()
  db = get_db()

  try:
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  
  except:
    print(sys.exc_info()[0])
    db.rollback()

    return jsonify(message = 'Cannot create post'), 500
  
  return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods = ['PUT']) # Update post route, <id> passes id as a parameter
@login_required
def update(id):
  data = request.get_json()
  db = get_db()

  try:
    post = db.query(Post).filter(Post.id == id).one() # Find the post given the id by filtering the results
    post.title = data['title']
    db.commit()
  
  except:
    print(sys.exc_info()[0])
    db.rollback()

    return jsonify(message = "Post not found, please try again."), 404
  
  return '', 204

@bp.route('/posts/<id>', methods = ['DELETE']) # Delete post route
@login_required
def delete(id):
  db = get_db()

  try:
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()

  except:
    print(sys.exc_info()[0])
    db.rollback()

    return jsonify(message = 'Post not found.'), 404
  
  return '', 204