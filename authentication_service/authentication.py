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

""""
VERSIONE CON JWT TOKEN 
from flask import Flask, jsonify, request
import jwt

app = Flask(__name__)

# Chiave segreta per generare e verificare i token JWT
SECRET_KEY = 'your_secret_key'

# Funzione per generare il token JWT
def generate_token(user_id):
    token = jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')
    return token

# Route per l'autenticazione e la generazione del token JWT
@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"success": False, "error": "User ID missing"}), 400

    # Qui puoi eseguire controlli aggiuntivi, verifiche dell'utente, etc.
    # ...

    token = generate_token(user_id)
    return jsonify({"success": True, "token": token.decode('utf-8')}), 200


# Route per verificare la validità del token JWT
@app.route('/verify_token', methods=['POST'])
def verify_token():
    token = request.json.get('token')

    if not token:
        return jsonify({"success": False, "error": "Token missing"}), 400

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        # Qui puoi eseguire ulteriori operazioni in base all'ID dell'utente estratto dal token
        return jsonify({"valid": True, "user_id": user_id})
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "error": "Invalid token"}), 401


if __name__ == '__main__':
    app.run(port=5002)  # Puoi scegliere una porta diversa se necessario
"""