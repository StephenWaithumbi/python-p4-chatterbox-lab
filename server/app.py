from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods= ['POST', 'GET'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by('created_at').all()]
        response = make_response(
            jsonify(messages), 200
        )       
        return response
    
    elif request.method == 'POST':
        data = request.get_json()

        try:
            new_message = Message(
                body = data.get('body'),
                username = data.get('username')
            )
            db.session.add(new_message)
            db.session.commit
            response = make_response(new_message.to_dict(), 201)
        except Exception as e:
            response = make_response({'Error': 'Failed to create message', 'message': str(e)}, 400)
        return response    

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()    

    if not message:
        return make_response({'Error': 'Message not found'}, 404)
    
    if request.method == 'PATCH':
        data = request.get_json()

        try:
            if 'body' in data:
                message.body = data['body']
            db.session.commit()
            response = make_response(message.to_dict(), 200)
        except Exception as e:
            response = make_response({'Error': 'Failed to update message', 'Message': str(e)}, 400)
        return response
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(message)
            db.session.commit()
            response = make_response({'Message': 'Message deleted successfully'}, 200)
        except Exception as e:
            response = make_response({'Error': 'Failed to delete the message', 'Message': str(e)}, 400)
        return response
        

        

if __name__ == '__main__':
    app.run(port=5555)
