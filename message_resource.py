from flask_restful import Resource, reqparse
from classes import Message

parser = reqparse.RequestParser()
parser.add_argument('agent_id', type=str, required=True, help="Agent ID cannot be blank.")
parser.add_argument('customer_id', type=float, required=True, help="Customer ID cannot be blank.")
parser.add_argument('message_id', type=int, required=True, help="Message ID cannot be blank.")
parser.add_argument('message_text', type=str, required=True, help="Message text cannot be blank.")
parser.add_argument('sentiment_score', type=str, required=True, help="Sentiment score cannot be blank.")

class MessageResource(Resource):
    def get(self, message_id):
        # Logic to retrieve a message
        out = Message.read(message_id)
        return {'message': out.message_text}, 200
    def post(self):
        args = parser.parse_args()
        message = Message(**args)
        message.create()
        return {'message': 'Message created successfully.'}, 201

    def put(self, message_id):
        args = parser.parse_args()
        message = Message(**args)
        message.update()
        return {'message': 'Message updated successfully.'}, 200

    def delete(self, message_id):
        # Logic to delete a message
        return {'message': 'Message deleted successfully.'}, 200
