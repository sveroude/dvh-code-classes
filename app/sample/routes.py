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

@app.route('/code-class/<int:id>/')
def codeClass(id):
    codeClass = session.query(CodeClass).filter_by(id = id).one()
    return render_template('code-class.html', codeClass = codeClass)

@app.route('/code-class/new/', methods=['GET', 'POST'])
def newCodeClass():
    if request.method == 'POST':
        newCodeClass = CodeClass(title=request.form['title'],
            date=request.form['date'],
            speaker=request.form['speaker'],
            description=request.form['description'])
        session.add(newCodeClass)
        session.commit()
        flash('new code class created!')
        return redirect(url_for('codeClasses'))
    else:
        return render_template('new-code-class.html')

@app.route('/code-class/<int:id>/edit/', methods=['GET', 'POST'])
def editCodeClass(id):
    editedCodeClass = session.query(CodeClass).filter_by(id = id).one()
    if request.method == 'POST':
        if request.form['title']:
            editedCodeClass.title = request.form['title']
        if request.form['date']:
            editedCodeClass.date = request.form['date']
        if request.form['speaker']:
            editedCodeClass.speaker = request.form['speaker']
        if request.form['description']:
            editedCodeClass.description = request.form['description']
        session.add(editedCodeClass)
        session.commit()
        flash('code class updated!')
        return redirect(url_for('codeClass', id = id))
    else:
        return render_template('edit-code-class.html', codeClass = editedCodeClass)

@app.route('/code-class/<int:id>/delete/', methods=['GET', 'POST'])
def deleteCodeClass(id):
    codeClassToDelete = session.query(CodeClass).filter_by(id = id).one()
    if request.method == 'POST':
        session.delete(codeClassToDelete)
        session.commit()
        flash('code class deleted!')
        return redirect(url_for('codeClasses'))
    else:
        return render_template('delete-code-class.html', codeClass = codeClassToDelete)

# if the script gets executed within the Python interpreter (and not as
# imported module)
if __name__ == '__main__':
    # add a secret key which Flask will use to create sessions for the user
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8899)
