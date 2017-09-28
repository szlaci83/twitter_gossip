#failed attempt :(
import threading
from flask import Flask, jsonify

import streaming
crypto_filter = ['bitcoin', 'ethereum', 'ETH', 'BTC']

app = Flask(__name__)

@app.route('/gossip/health', methods=['GET'])
def get_health():
    if app.streaming_thread.is_alive():
        return jsonify({'Health': 'OK'})
    else:
        return jsonify({'Health': 'Its dead '})

if __name__ == '__main__':
    app.streaming_thread = threading.Thread(name='daemon', target=streaming.do_filter)
    app.streaming_thread.setDaemon(True)
    app.run(debug=True)