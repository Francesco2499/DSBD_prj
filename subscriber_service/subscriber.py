from flask import Flask, jsonify, request
from helpers import kafkaHelpers
import threading
import jwt

app = Flask(__name__)

# Chiave segreta per verificare i token JWT
SECRET_KEY = 'your_secret_key'


# Funzione per verificare il token JWT
def verify_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        # Qui potresti fare ulteriori verifiche, come verificare l'accesso ai topic, etc.
        return True, user_id
    except jwt.ExpiredSignatureError:
        return False, None
    except jwt.InvalidTokenError:
        return False, None


@app.route('/subscribe', methods=['GET'])
def subscribe_to_chosen_topic():
    try:
        access_token = request.headers.get('Authorization')  # Ottieni il token di accesso dall'header Authorization

        if not access_token or not access_token.startswith('Bearer '):
            return jsonify({"success": False, "error": "Invalid token"}), 401

        token = access_token.split(' ')[1]

        is_valid, user_id = verify_token(token)
        if is_valid:
            category = request.args.get('category', 'general')  # Se non specificata, default a 'news'
            topic_name = f'{category}_topic'

            thread = threading.Thread(target=kafkaHelpers.subscribe_to_topic, args=(topic_name,))
            thread.start()

            return jsonify({'success': True, 'message': f'Subscribed to {category} topic successfully'})
        else:
            return jsonify({'success': False, 'error': 'Authentication failed'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
