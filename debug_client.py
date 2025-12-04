from app import app as flask_app
from models import init_db

flask_app.config['TESTING'] = True
flask_app.config['DATABASE'] = 'debug_test.db'
init_db(flask_app)

with flask_app.test_client() as client:
    resp = client.post('/register', data={'username': 'alice', 'email': 'alice@example.com', 'password': 's3cret'}, follow_redirects=True)
    print('STATUS:', resp.status_code)
    print(resp.get_data(as_text=True))
