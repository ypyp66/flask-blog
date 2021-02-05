import os
from flask      import Flask, jsonify, request, render_template
from sqlalchemy import create_engine, text


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

import auth 
app.register_blueprint(auth.bp)
import db 
db.init_app(app)
import blog
app.register_blueprint(blog.bp)
import board
app.register_blueprint(board.bp)

# a simple page that says hello
@app.route('/')
def toHome():
    return render_template('home.html')