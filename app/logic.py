from app import mongo
from utils import ocr


def perform_ocr(img_path):

    # Perform ocr
    result = ocr(img_path)

    # Save result to mongo
    mongo.db.history.insert_one({
        "text": result
    })

    # Return result
    return result


class LoginService:
    def __init__(self):
        pass

    def login(self, username, password):
        return True