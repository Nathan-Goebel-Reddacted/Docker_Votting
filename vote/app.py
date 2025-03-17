from flask import Flask, render_template, request, make_response
from redis import Redis
import os
import socket
import random
import json
import logging

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

app.logger.setLevel(logging.INFO)

def get_redis():
    if not hasattr(Flask, 'redis'):
        #adapter redis pour utiliser les variable environementale
        redis_host = os.getenv("REDIS_HOST", "localhost")   
        Flask.redis = Redis(host=redis_host, db=0, socket_timeout=5)
    return Flask.redis

@app.route("/", methods=['POST', 'GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        app.logger.info('Received vote for %s', vote)
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    #utilisation des variable environementale, au cas ou.
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")  
    port = int(os.getenv("FLASK_RUN_PORT", 8080))  
    app.run(host=host, port=port, debug=True, threaded=True)
