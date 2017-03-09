from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# create the application instance
app = Flask(__name__)

SESSION_KEY = os.environ.get("SESSION_KEY")

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# login to Google API using OAuth2 credentials
client = gspread.authorize(creds)
# open spreadsheet by its title
codeClassRecords = client.open("dvh-activities").worksheet('classes')

@app.route('/')
@app.route('/code-classes/')
def codeClasses():
    codeClasses = codeClassRecords.get_all_records()
    return render_template('code-classes.html', codeClasses = codeClasses)

@app.route('/code-class/<title>/', methods=['GET', 'POST'])
def codeClass(title):
    if request.method == 'POST':
        row = codeClassRecords.find(title).row
        rating = request.form['rating']

        codeClassRecords.update_cell(row, 5, rating)
        return redirect(url_for('codeClasses'))

    else:
        keys = codeClassRecords.row_values(1)
        values = codeClassRecords.row_values(codeClassRecords.find(title).row)
        # Create a codeClass dictionary from the keys and correct row values
        codeClass = dict(zip(keys, values))

        return render_template('code-class.html', codeClass = codeClass)

@app.route('/code-class/new/', methods=['GET', 'POST'])
def newCodeClass():
    if request.method == 'POST':
        numberOfRows = codeClassRecords.row_count
        newRow = numberOfRows + 1
        formData = [request.form['title'], request.form['speaker'], request.form['date'], request.form['description']]

        codeClassRecords.insert_row(formData, newRow)
        return redirect(url_for('codeClasses'))
    else:
        return render_template('new-code-class.html')

@app.route('/code-class/<title>/edit/', methods=['GET', 'POST'])
def editCodeClass(title):
    if request.method == 'POST':
        codeClassRow = codeClassRecords.find(title).row
        cellList = codeClassRecords.range("B%s:E%s" % (codeClassRow, codeClassRow))
        formData = [request.form['title'], request.form['speaker'], request.form['date'], request.form['description']]

        for i, cell in enumerate(cellList):
            cell.value = formData[i]

        codeClassRecords.update_cells(cellList)

        return redirect(url_for('codeClass', title = request.form['title']))
    else:
        keys = codeClassRecords.row_values(1)
        values = codeClassRecords.row_values(codeClassRecords.find(title).row)
        # Create a codeClass dictionary from the keys and correct row values
        codeClassToEdit = dict(zip(keys, values))

        return render_template('edit-code-class.html', codeClass = codeClassToEdit)

@app.route('/code-class/<title>/delete/', methods=['GET', 'POST'])
def deleteCodeClass(title):
    if request.method == 'POST':
        codeClass = codeClassRecords.find(title).row

        codeClassRecords.delete_row(codeClass)
        return redirect(url_for('codeClasses'))
    else:
        keys = codeClassRecords.row_values(1)
        values = codeClassRecords.row_values(codeClassRecords.find(title).row)
        # Create a codeClass dictionary from the keys and correct row values
        codeClassToDelete = dict(zip(keys, values))

        return render_template('delete-code-class.html', codeClass = codeClassToDelete)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# if the script gets executed within the Python interpreter (and not as
# imported module)
if __name__ == '__main__':
    # add a secret key which Flask will use to create sessions for the user
    app.secret_key = SESSION_KEY
    app.debug = True
    app.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 8000))) # default)
