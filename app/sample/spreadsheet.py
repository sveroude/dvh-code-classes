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
sheet = client.open("dvh-code-classes").sheet1

@app.route('/')
@app.route('/code-classes/')
def codeClasses():
    codeClasses = sheet.get_all_records()
    return render_template('code-classes.html', codeClasses = codeClasses)

@app.route('/code-class/<id>/')
def codeClass(id):
    codeClasses = sheet.get_all_records()
    classId = sheet.find(id).row - 2
    codeClass = codeClasses[classId]
    return render_template('code-class.html', codeClass = codeClass)

# if the script gets executed within the Python interpreter (and not as
# imported module)
if __name__ == '__main__':
    # add a secret key which Flask will use to create sessions for the user
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8899)
