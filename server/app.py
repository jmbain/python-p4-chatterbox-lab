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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = Message.query.all()
        return [message.to_dict() for message in all_messages], 200
    
    if request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data.get('body'),
            username=data.get('username')
        )
        
        db.session.add(new_message)
        db.session.commit()

        return new_message.to_dict(), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    #Query and filter for Message objects whose id attribute matches the id parameter from the route
    msg = Message.query.filter(Message.id == id).first()
    if request.method == 'PATCH': 
        #return error message and 404 if msg not found
        if msg is None:
            return {"error": "Message not found..."}, 404
        # get json from request object
        data = request.get_json()
        #update the body of msg with the body in data
        if 'body' in data:
            msg.body = data['body']
        #add and commit to db
        db.session.add(msg)
        db.session.commit()
        #return SERIALIZED msg after updated
        return msg.to_dict(), 200
    
    if request.method == "DELETE":
        db.session.delete(msg)
        db.session.commit()
        return {}, 200

if __name__ == '__main__':
    app.run(port=5555)
