from flask import Blueprint, render_template, session, redirect # Blueprint = express router
from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/') # Blueprint is used to aggregate routes

@bp.route('/')
def index():
  db = get_db()
  posts = db.query(Post).order_by(Post.created_at.desc()).all() # Formatting matters
  # to clean up and order each query in python, use () around the specifications
  # posts = (
    #db
      #.query(Post)
      #.order_by(Post.created_at.desc())
      #.all()
  #)
  return render_template(
    'homepage.html',
    posts = posts,
    loggedIn = session.get('loggedIn') # Sends session info
  ) # Use render_template to render a template upon navigating to the page.

@bp.route('/login')
def login():
  if session.get('loggedIn') is None:
    return render_template('login.html')
  return redirect('/dashboard')

@bp.route('/post/<id>') # <id> becomes the variable to be passed into single()
def single(id):
  db = get_db()
  post = db.query(Post).filter(Post.id == id).one()

  return render_template(
    'single-post.html',
    post = post,
    loggedIn = session.get('loggedIn') # Sends session info
  )