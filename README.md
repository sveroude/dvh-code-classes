# DVH Activities

An overview of all DVH activities. This project uses the [gspread](https://github.com/burnash/gspread)
Python package to read, write, and delete data from a Google Spreadsheet.

## Getting started

``` bash
git clone git@github.com:sveroude/dvh-code-classes.git
```

## Google Drive API and Service Accounts

Ask the owner of this project for access to the dvh-activities spreadsheet.

To programmatically access your spreadsheet, you’ll need to create a service
account and OAuth2 credentials from the Google API Console:

- Go to the [Google APIs Console](https://console.developers.google.com/).
- Create a new project.
- Click *Enable API*. Search for and enable the Google Drive API.
- *Create credentials* for a *Web Server* to access *Application Data*.
- Name the service account and grant it a *Project* Role of *Editor*.
- Download the JSON file.
- Rename the JSON file to `credentials.json`. Copy the file and paste it in the root directory

There is one last required step to authorize the app:
- Find the `client_email` inside` credentials.json`.
- In the spreadsheet, click the Share button in the top right.
- Paste the client email into the People field to give it edit rights.
- Hit Send.

## Project setup

This project uses [node](https://nodejs.org/en/) for watching source files, building its assets and starting a server.

Install dependencies:

``` bash
$ npm install
```

A virtual environment is used to create a Python environment segregated from your system wide Python installation.

Create a virtual environment:

``` bash
$ virtualenv venv
```

Install the project requirements from the virtual environment:

``` bash
$ source venv/bin/activate
$ pip install -r requirements.txt
$ deactivate
```

## Development

### Activate virtual environment

Activate the virtual environment:

``` bash
$ source venv/bin/activate
```

The name of the current virtual environment will now appear on the left of the
prompt to let you know that it’s active.

### Start

Start the server:

``` bash
$ npm run start
```

### Watch

Watch LESS and JS files:

``` bash
$ npm run watch
```

### Deactivate virtual environment

If you are done working in the virtual environment for the moment, you can deactivate it:

``` bash
$ deactivate
```
