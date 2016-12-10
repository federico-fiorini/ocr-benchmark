#!.env/bin/python
from app.logic import delete_expired_images

if __name__ == "__main__":
    # Delete expired images
    delete_expired_images()
