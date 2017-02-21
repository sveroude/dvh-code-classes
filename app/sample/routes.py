from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# create the application instance
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, CodeClass

engine = create_engine('sqlite:///codeclasses.db')
Base.metadata.bind = engine

# Establish a link of communication between the program and database
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/code-classes/')
def codeClasses():
    codeClasses = session.query(CodeClass).all()
    return render_template('code-classes.html', codeClasses = codeClasses)

# if the script gets executed within the Python interpreter (and not as
# imported module)
if __name__ == '__main__':
    # add a secret key which Flask will use to create sessions for the user
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8899)
