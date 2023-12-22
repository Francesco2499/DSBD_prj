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

    token = generate_token(user_id)
    return jsonify({"success": True, "token": token}), 200


# Route per verificare la validità del token JWT
@app.route('/verify_token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    print(token)
    if not token:
        return jsonify({"success": False, "error": "Token missing"}), 400

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        return jsonify({"valid": True, "user_id": user_id})
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "error": "Invalid token"}), 401


if __name__ == '__main__':
    app.run(debug=True, port=5002)
