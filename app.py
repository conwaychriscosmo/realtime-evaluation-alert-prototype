from flask import Flask
from flask_restful import Api
from message_resource import MessageResource

app = Flask(__name__)
api = Api(app)

# Add the Message resource to the API
api.add_resource(MessageResource, '/message')

if __name__ == '__main__':
    print("Available endpoints:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
    app.run(debug=True)
