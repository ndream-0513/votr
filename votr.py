from flask import Flask
from models import db

votr = Flask(__name__)

votr.config.from_object('config')

db.init_app(votr)
with votr.app_context():
    db.create_all()

@votr.route('/')
def home():
    return 'hello world'

if __name__ == '__main__':
    votr.run(host='0.0.0.0')
