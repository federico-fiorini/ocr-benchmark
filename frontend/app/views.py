from app import app
from external import BackEndService
from flask import request, session, redirect, url_for, render_template

import os
import time

SALT = "fV3Q26FcTz2DsHFf"


@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route("/", methods=['GET', 'POST'])
def login():
    
    # If logged in already: redirect to dashboard page
    if 'logged_in' in session and session['logged_in'] == True:
        return redirect(url_for('TODO'))  # TODO: redirect to main page

    # If POST: check login
    if request.method == 'POST':

        username = request.form['inputName']
        password = request.form['hash']

        service = BackEndService()
        correct_login = service.login(username, password)

        # If not logged in: show error
        if not correct_login:
            session['logged_in'] = False
            return render_template('login.html', error="Invalid credentials", salt=SALT)

        # Otherwise: redirect to dashboard page
        session['logged_in'] = True
        return redirect(url_for('TODO'))  # TODO: redirect to main page

    # If GET
    return render_template('login.html', error=None, salt=SALT)


@app.route("/TODO", methods=['GET'])  # TODO: render main dashboard page
def TODO():

    # Check if logged in
    if 'logged_in' not in session or session['logged_in'] == False:
        return redirect(url_for('login'))

    pass
