from flask import Flask, jsonify, redirect, url_for, request
from authlib.integrations.flask_client import OAuth
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'segreto'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='your-client-id',
    client_secret='your-client-secret',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    refresh_token_params=None,
    scope='profile email',
    redirect_uri='http://localhost:5000/login/google/authorize',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',
    client_kwargs={'scope': 'openid profile email'}
)

# Funzione per verificare il token di accesso di Google
def verify_google_token(token):
    google_validation_url = f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}'
    response = requests.get(google_validation_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/login/google/authorize')
def authorize_google():
    try:
        token = google.authorize_access_token()
        user_info = google.parse_id_token(token)

        # Ottieni il token di accesso fornito da Google
        access_token = token['access_token']

        # Verifica il token di accesso di Google
        verified_info = verify_google_token(access_token)

        if verified_info:
            return jsonify({'user_info': verified_info, 'message': 'Autorizzato'})
        else:
            return jsonify({'error': 'Token di accesso Google non valido'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
