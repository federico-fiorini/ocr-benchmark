from app import app
from utils import perform_ocr, allowed_file, create_thumbnail, unique_filename
import os
from flask import session, url_for
from datetime import datetime
from models import Users, History
import time
import isodate


def init_test_users(json_file):
    """
    Init mongo database with test users
    :param json_file:
    :return:
    """
    import json

    with open(json_file) as user_data:
        # Load json file
        test_users = json.load(user_data)

        # Check if each user exists and add it if not
        for test_user in test_users:
            user = Users.get_user(test_user['username'])

            if user is not None:
                continue

            # Save new user
            user = Users()
            user.username = test_user['username']
            user.password = test_user['password']
            user.save()


def login_user(username, password):
    """
    Check if username and password are correct
    :param username:
    :param password:
    :return:
    """

    # Find user and check password
    user = Users.get_user(username)

    is_correct = user is not None and user.password == password

    # Set session values
    session['logged_in'] = is_correct
    session['user'] = username if is_correct else None

    return is_correct


def save_history(text, thumbnail, filenames):
    """
    Save ocr result to mongo
    :param text:
    :param thumbnail:
    :return:
    """

    if 'user' not in session:
        return

    username = session['user']
    timestamp = isodate.datetime_isoformat(datetime.now())

    # Create new history object
    new_history = History()
    new_history.user = username
    new_history.text = text
    new_history.thumbnail = thumbnail
    new_history.timestamp = timestamp
    new_history.source_files = filenames

    # Save to mongo
    new_history.save()


def get_history():

    if 'user' not in session:
        return []

    username = session['user']

    # Retrieve history for user
    history = History.get_history_by_user(username)

    # Return history object
    return map(lambda x: {
        'text': x['text'],
        'timestamp': x['timestamp'],
        'thumbnail': x['thumbnail'],
        'source-files': map(lambda y: url_for('image', filename=y), x['source_files'])
    }, history)


def save_and_get_text(files):
    """
    Save image, perform ocr, save result to mongo
    :param files:
    :return:
    """

    text = []
    times = []
    filenames = []
    first_filepath = ""

    for i, file in enumerate(files):

        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):

            start_time = time.time()

            # Make the filename safe, remove unsupported chars
            filename = unique_filename(file.filename)
            filenames.append(filename)

            # Save file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if i == 0:
                first_filepath = filepath

            # Perform ocr to get text
            result = perform_ocr(filepath)
            text.append(result)

            # Get time delta in seconds
            end_time = time.time()
            times.append(end_time - start_time)

    # Join in unique text
    text = "\n".join(text)

    # Create thumbnail of first image
    thumbnail = create_thumbnail(first_filepath)

    # Save to mongo
    save_history(text, thumbnail, filenames)

    return text, times
