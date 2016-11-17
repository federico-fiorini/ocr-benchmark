#!.env/bin/python
from app import app
from OpenSSL import SSL
import sys

try:
    port = int(sys.argv[1])
except IndexError:
    port = 5000


if __name__ == "__main__":
    context = ('certificate.crt', 'private.key')
    app.run(debug=True, port=port, ssl_context=context)
