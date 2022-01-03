from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with, request
from flask_mongoengine import MongoEngine


# initializing and setting up Flask, API, and DB
app = Flask(__name__)
api = Api(app)
# DB_URI = f'mongodb+srv://user:{DB_PASSWORD}@cluster0.ofzgt.mongodb.net/{DB_NAME}?retryWrites=true&w=majority'
# app.config['MONGODB_HOST'] = DB_URI             # connects to an atlas-hosted (cloud) MongoDB server (which is only set to accept connections on my IP)
app.config['MONGODB_SETTINGS'] = {              # connects to a locally hosted MongoDB server
    'db': 'MongoDBZ',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)


# simple auth system setup
X_API_KEYS = set(['m8hd936ro04h9fq1'])


# defining the DBZ Character document (data model)
class CharacterModel(db.Document):
    _id = db.IntField(primary_key=True)
    name = db.StringField(required=True)
    level = db.IntField(required=True)
    powers = db.ListField(db.StringField(), required=True)

    def __repr__(self):
        return f'Character(_id = {self._id}, name = {self.name}, level = {self.level}, powers = {self.powers})'


# defining the request parsers
characterPostArgs = reqparse.RequestParser()
characterPostArgs.add_argument('name', type=str, help='Name of the character', required=True)
characterPostArgs.add_argument('level', type=int, help='Power level of the character', required=True)
characterPostArgs.add_argument('powers', type=str, default=['punch'], action='append')

characterPutArgs = reqparse.RequestParser()
characterPutArgs.add_argument('name', type=str)
characterPutArgs.add_argument('level', type=int)
characterPutArgs.add_argument('powers', type=str, action='append')


# defining the resource fields
resource_fields_character = {
    '_id': fields.Integer,
    'name': fields.String,
    'level': fields.Integer,
    'powers': fields.List(fields.String),
}


# defining the 'Character' resource
class Character(Resource):
    @marshal_with(resource_fields_character)
    def get(self, _id):
        if request.headers.get('x-api-key') not in X_API_KEYS:
            abort(401, message=f'Please provide a valid key at the header "x-api-key"...')

        result = CharacterModel.objects(_id=_id).first()
        if not result:
            abort(404, message=f'Could not find character with ID {_id}...')

        return result, 200

    @marshal_with(resource_fields_character)
    def post(self, _id):
        if request.headers.get('x-api-key') not in X_API_KEYS:
            abort(401, message=f'Please provide a valid key at the header "x-api-key"...')

        if CharacterModel.objects(_id=_id).first():
            abort(409, message=f'Character with ID {_id} already taken...')

        args = characterPostArgs.parse_args()
        result = CharacterModel(_id=_id, name=args['name'], level=args['level'], powers=args['powers'])
        result.save()
        return result, 201

    @marshal_with(resource_fields_character)
    def put(self, _id):
        if request.headers.get('x-api-key') not in X_API_KEYS:
            abort(401, message=f'Please provide a valid key at the header "x-api-key"...')

        result = CharacterModel.objects(_id=_id).first()
        if not result:
            abort(404, message=f'Could not find character with ID {_id}...')

        args = characterPutArgs.parse_args()
        if args['name']:
            result.name = args['name']
        if args['level']:
            result.level = args['level']
        if args['powers']:
            result.powers = args['powers']
        result.save()
        return result, 200
        # return '', 204                              # alternate way to respond (without content, b/c response code)

    @marshal_with(resource_fields_character)
    def delete(self, _id):
        if request.headers.get('x-api-key') not in X_API_KEYS:
            abort(401, message=f'Please provide a valid key at the header "x-api-key"...')

        result = CharacterModel.objects(_id=_id).first()
        if not result:
            abort(404, message=f'Could not find character with ID {_id}...')

        result.delete()
        # return result, 200                          # way to respond (with content, b/c response code)
        return '', 204


# defining the 'Characters' resource
class Characters(Resource):
    @marshal_with(resource_fields_character)
    def get(self):
        if request.headers.get('x-api-key') not in X_API_KEYS:
            abort(401, message=f'Please provide a valid key at the header "x-api-key"...')
            
        return [character for character in CharacterModel.objects], 200


# adding the resources to the API
api.add_resource(Character, '/api/character/<int:_id>')
api.add_resource(Characters, '/api/characters')


# running the Flask app
if __name__ == '__main__':
    app.run(debug=True)