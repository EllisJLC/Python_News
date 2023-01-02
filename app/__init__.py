from flask import Flask

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
  
  return app