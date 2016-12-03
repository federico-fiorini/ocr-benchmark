#!.env/bin/python
from app import app
from OpenSSL import SSL
import sys

try:
    port = int(sys.argv[1])
except IndexError:
    port = 5000


if __name__ == "__main__":
    context = ('credentials/certificate.crt', 'credentials/private.key')
    app.run(debug=True, host='0.0.0.0', port=port, ssl_context=context)
