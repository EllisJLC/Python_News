from flask import Blueprint, render_template # Blueprint = express router

bp = Blueprint('home', __name__, url_prefix='/') # Blueprint is used to aggregate routes

@bp.route('/')
def index():
  return render_template('homepage.html') # Use render_template to render a template upon navigating to the page.

@bp.route('/login')
def login():
  return render_template('login.html')