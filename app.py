from flask import Flask
from flask_restful import Api
from message_resource import MessageResource
from flask_sqlalchemy import SQLAlchemy
from exts import db
from Auth.routes import *
from classes import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prototype.db'
api = Api(app)
app.register_blueprint(bp)
# Add the Message resource to the API
api.add_resource(MessageResource, '/message/<int:message_id>', '/message')

if __name__ == '__main__':
    print("Available endpoints:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
