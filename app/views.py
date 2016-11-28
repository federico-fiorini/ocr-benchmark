from app import app
from external import BackEndService
from flask import request, session, redirect, url_for, render_template
from werkzeug import secure_filename
import requests
import os
import time

SALT = "fV3Q26FcTz2DsHFf"

# This is the path to the upload directory
#app.config['UPLOAD_FOLDER'] = url_for('static', filename='uploads/')

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

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
        try:       
            service = BackEndService()
            correct_login = service.login(username, password)

            # If not logged in: show error
            if not correct_login:
                session['logged_in'] = False
                return render_template('login.html', error="Invalid credentials", salt=SALT)
        except requests.ConnectionError as e:
            session['logged_in'] = False
            return render_template('login.html', error="Service not available, try again later", salt=SALT)
        # Otherwise: redirect to dashboard page
        session['logged_in'] = True
        return redirect(url_for('dashboard'))

    # If GET
    return render_template('login.html', error=None, salt=SALT)


@app.route("/dashboard", methods=['GET'])  # TODO: add functions 
def dashboard():

    # Check if logged in
    if 'logged_in' not in session or session['logged_in'] == False:
        return redirect(url_for('login'))

    return render_template('dashboard.html')



@app.route("/camera", methods=['GET'])  # TODO: add functions 
def camera():

    # Check if logged in
    if 'logged_in' not in session or session['logged_in'] == False:
        return redirect(url_for('login'))

    return render_template('camera.html')



@app.route("/ocr", methods=['GET', 'POST'])  # TODO: add functions 
def ocr():

    # Check if logged in
    if 'logged_in' not in session or session['logged_in'] == False:
        return redirect(url_for('login'))

    filenames = getFiles()
    return render_template('ocr.html', files=filenames)



@app.route("/result", methods=['GET', 'POST'])  # TODO: add functions 
def result():

    # Check if logged in
    if 'logged_in' not in session or session['logged_in'] == False:
        return redirect(url_for('login'))
	
    result = request.form['ocr_result']
    return render_template('result.html', result=result)

@app.route("/benchmark", methods=['GET'])  # TODO: add functions 
def benchmark():

    # Check if logged in
    if 'logged_in' not in session or session['logged_in'] == False:
        return redirect(url_for('login'))

    return render_template('benchmark.html')

def getFiles():
    # Get the name of the uploaded file
    files = request.files.getlist('pics[]')
    filenames = []
	
    for file in files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            filepath = "app" + os.path.join(url_for('static', filename='uploads/'), filename)
            file.save(filepath)
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file