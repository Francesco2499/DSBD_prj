from flask import Flask, jsonify, request
from helpers import kafkaHelpers
import threading
import jwt
import sys

sys.path.append("helpers/")
sys.path.append("configs/")

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

        category = request.args.get('category', 'general')  # Se non specificata, default a 'news'
        topic_name = f'{category}_topic'

        thread = threading.Thread(target=kafkaHelpers.subscribe_to_topic, args=(topic_name,))
        thread.start()

        return jsonify({'success': True, 'message': f'Subscribed to {category} topic successfully'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)
