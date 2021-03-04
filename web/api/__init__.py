import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


@app.route('/')
def index():
    return jsonify({'status': 'Isso deu certo!'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
