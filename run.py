#!.env/bin/python
from app import app
import sys

try:
    port = int(sys.argv[1])
except IndexError:
    port = 5000


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
