Test artifacts and sample commands

- Register (browser recommended due to CSRF): Open `http://127.0.0.1:5000/register` and submit the form.
- Login: Open `http://127.0.0.1:5000/login` and submit credentials.

Curl examples (will fail due to CSRF unless CSRF token included):

```
curl -i -X POST -F "username=alice" -F "email=alice@example.com" -F "password=s3cret" http://127.0.0.1:5000/register
```

API endpoints `/api/register` and `/api/login` are not implemented; expect 404.
