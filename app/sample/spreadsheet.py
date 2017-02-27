from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# create the application instance
app = Flask(__name__)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
# login to Google API using OAuth2 credentials
client = gspread.authorize(creds)
# open spreadsheet by its title
codeClassRecords = client.open("dvh-activities").worksheet('code-classes')
codeTalkRecords = client.open("dvh-activities").worksheet('code-talks')

@app.route('/')
@app.route('/activities/')
def codeClasses():
    codeClasses = codeClassRecords.get_all_records()
    codeTalks = codeTalkRecords.get_all_records()
    return render_template('activities.html', codeClasses = codeClasses, codeTalks = codeTalks)

@app.route('/code-class/<id>/')
def codeClass(id):
    codeClasses = codeClassRecords.get_all_records()
    classId = codeClassRecords.find(id).row - 2
    codeClass = codeClasses[classId]
    return render_template('code-class.html', codeClass = codeClass)

@app.route('/code-class/new/', methods=['GET', 'POST'])
def newCodeClass():
    if request.method == 'POST':
        row = codeClassRecords.row_count
        newRow = row + 1
        codeClass = [
            request.form['title'],
            row,
            request.form['speaker'],
            request.form['date'],
            request.form['description']
        ]

        codeClassRecords.insert_row(codeClass, newRow)
        return redirect(url_for('codeClasses'))
    else:
        return render_template('new-code-class.html')

@app.route('/code-class/<id>/edit/', methods=['GET', 'POST'])
def editCodeClass(id):
    codeClasses = codeClassRecords.get_all_records()
    row = codeClassRecords.find(id).row
    classId = row - 2
    codeClassToEdit = codeClasses[classId]

    if request.method == 'POST':
        print codeClassToEdit
        codeClassRecords.update_cell(row, 1, request.form['title'])
        codeClassRecords.update_cell(row, 3, request.form['speaker'])
        codeClassRecords.update_cell(row, 4, request.form['date'])
        codeClassRecords.update_cell(row, 5, request.form['description'])

        return redirect(url_for('codeClass', id = id))
    else:
        return render_template('edit-code-class.html', codeClass = codeClassToEdit)

@app.route('/code-class/<id>/delete/', methods=['GET', 'POST'])
def deleteCodeClass(id):
    codeClasses = codeClassRecords.get_all_records()
    codeClass = codeClassRecords.find(id).row
    classId = codeClass - 2
    codeClassToDelete = codeClasses[classId]
    if request.method == 'POST':
        codeClassRecords.delete_row(codeClass)
        return redirect(url_for('codeClasses'))
    else:
        return render_template('delete-code-class.html', codeClass = codeClassToDelete)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# if the script gets executed within the Python interpreter (and not as
# imported module)
if __name__ == '__main__':
    # add a secret key which Flask will use to create sessions for the user
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8899)
