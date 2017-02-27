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
    print codeClassRecords.col_values(2)
    return render_template('activities.html', codeClasses = codeClasses, codeTalks = codeTalks)

@app.route('/code-class/<id>/')
def codeClass(id):
    keys = codeClassRecords.row_values(1)
    values = codeClassRecords.row_values(codeClassRecords.find(id).row)
    codeClass = dict(zip(keys, values))

    return render_template('code-class.html', codeClass = codeClass)

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
