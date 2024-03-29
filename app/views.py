from app import app
from logic import login_user, save_and_get_text, get_history, get_image_encoded
from flask import request, session, redirect, url_for, render_template, jsonify, make_response, abort

SALT = app.config['SALT']


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


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():

    # Check if logged in
    if 'logged_in' not in session or session['logged_in'] == False:
        return redirect(url_for('login'))

    # If POST: handle call
    if request.method == 'POST':

        files = request.files.getlist("files")

        print("received files: " + str(files))

        # Save files and get text
        result_text, times = save_and_get_text(files)

        return make_response(jsonify({'text': result_text, 'times': times}))

    # If GET render the page
    return render_template('dashboard.html')


@app.route("/history", methods=['GET'])
def history():
    """
    Endpoint to retrieve history of logged user
    :return:
    """
    history = get_history()
    return make_response(jsonify({'history': history}))


@app.route("/image/<filename>", methods=['GET'])
def image(filename):
    """
    Endpoint to retrieve source image by name
    :param filename:
    :return:
    """
    encoded_image = get_image_encoded(filename)

    if encoded_image is None:
        abort(404)

    return encoded_image


@app.route("/logout", methods=['GET'])
def logout():
    """
    Perform logout
    :return:
    """
    session['logged_in'] = False
    return redirect(url_for('login'))

