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
activityRecords = client.open("dvh-activities").worksheet('activities')

@app.route('/')
@app.route('/activities/')
def activities():
    activities = activityRecords.get_all_records()
    return render_template('activities.html', activities = activities)

@app.route('/activity/<title>/')
def activity(title):
    keys = activityRecords.row_values(1)
    values = activityRecords.row_values(activityRecords.find(title).row)
    activity = dict(zip(keys, values))

    return render_template('activity.html', activity = activity)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# if the script gets executed within the Python interpreter (and not as
# imported module)
if __name__ == '__main__':
    # add a secret key which Flask will use to create sessions for the user
    app.secret_key = SESSION_KEY # replace with env variable
    app.debug = True
    app.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 8000))) # default)
