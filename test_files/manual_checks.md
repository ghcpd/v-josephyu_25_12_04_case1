Manual checks and curl examples
================================

These are simple manual commands you can use while the server is running to exercise documented behavior.

Note: start the server first (see corrected_readme.md). For example:

  # via flask run
  export FLASK_APP=app.py
  flask run --host=0.0.0.0 --port=8080

Register using the HTML form or use an example curl POST to exercise form parameters (form-encoded):

  curl -X POST -d "username=test1" -d "email=test1@example.com" -d "password=password" http://127.0.0.1:5000/register

Login similarly:

  curl -X POST -d "username=test1" -d "password=password" http://127.0.0.1:5000/login

API endpoints under /api/* are NOT present in this repo — those requests will return 404.
