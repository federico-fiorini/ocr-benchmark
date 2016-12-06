from app import app
from logic import login_user, save_and_get_text, get_history
from flask import request, session, redirect, url_for, render_template, jsonify, make_response


SALT = app.config['SALT']


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
        return redirect(url_for('dashboard'))

    # If POST: check login
    if request.method == 'POST':

        username = request.form['inputName']
        password = request.form['hash']

        correct_login = login_user(username, password)

        # If not logged in: show error
        if not correct_login:
            return render_template('login.html', error="Invalid credentials", salt=SALT)

        # Otherwise: redirect to dashboard page
        return redirect(url_for('dashboard'))

    # If GET
    return render_template('login.html', error=None, salt=SALT)


@app.route("/dashboard", methods=['GET', 'POST'])  # TODO: add functions 
def dashboard():

    # Check if logged in
    if 'logged_in' not in session or session['logged_in'] == False:
        return redirect(url_for('login'))
     
    # If POST: handle call
    if request.method == 'POST':

        files = request.files.getlist("files")
 
        print("received files: " + str(files))

        # Save files and get text
        result_text = save_and_get_text(files)

        return make_response(jsonify({'text': result_text}))

    # If GET
    history = get_history()

    return render_template('dashboard.html')


@app.route("/logout", methods=['GET'])  # TODO: add functions
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

