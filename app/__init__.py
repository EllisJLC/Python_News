from flask import Flask
from app.routes import home, dashboard # Import by routing through directories with '.', possible to import home due to __init__.py renaming
from app.db import init_db
# can also use -> from app.routes.home import bp as home -> used if bp is not imported into the __init__.py

def create_app(test_config=None):
  # Set up app configuration
  app = Flask(__name__, static_url_path='/')
  app.url_map.strict_slashes = False
  app.config.from_mapping(
    SECRET_KEY = "super_secret_key"
  )

  @app.route('/hello') # Turns the hello() function into a route
  def hello():
    return 'hello world'
  
  app.register_blueprint(home)
  app.register_blueprint(dashboard)
  
  init_db(app)

  return app