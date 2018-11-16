from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_argon2 import Argon2
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

argon2 = Argon2(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

api = Api(app, version="1.0", title="Simple API",
        description="A Simple API",
    )
sm = api.namespace("sm", description="TODO operations")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    status = db.Column(db.String(10))

    def __repr__(self):
        return f'<User {self.username}>'

todo = sm.model('Todo', {
    'id': fields.Integer(readOnly=True, description='identifier'),
    'username': fields.String(required=True, description='name for user'),
    'email': fields.String(required=True, description='email for user'),
    'password': fields.String(required=True, description='password for user')
})

class TodoDAO:
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, userid=None):
        user_list = []

        if userid != None:
            user = User.query.filter_by(id=userid).first()
            if not user:
                user_list.append({
                    "response": "user doesn't exist"
                })
            else:
                user_list.append({
                        'id': user.id, 
                        'username': user.username, 
                        'email': user.email, 
                        'status': user.status
                    })
        else:
            user = User.query.all()
        
            for item in user:
                user_list.append({
                    'id': item.id, 
                    'username': item.username, 
                    'email': item.email, 
                    'status': item.status
                })
        
        return user_list
        
    def create(self, data):
        try:
            username = data["username"]
            email = data["email"]
            password = data["password"]

            user = User(username=username, 
                        email=email,
                        password_hash=argon2.generate_password_hash(password),
                        status = "pending")

            db.session.add(user)
            db.session.commit()

            return data
        except Exception as e:
            return {'response': 'username already exist'}

    def delete(self, userid):
        # User.query.filter_by(id=userid).delete()

        try:
            user = User.query.filter_by(id=userid).first()

            db.session.delete(user)
            db.session.commit()

        except:
            pass   
    
    def update(self, userid, data):
        try:
            username = data["username"]
            email = data["email"]
            password = data["password"]

            user = User.query.filter_by(id=userid).first()

            if user:
                user.username=username
                user.email=email
                user.password_hash=argon2.generate_password_hash(password)
                user.status = "pending"
                
                db.session.commit()

                return data
            else:
                return {'response': 'unsuccessfully'}
        except:
            return {'response': 'unsuccessfully'}

    def patch(self, userid):
        try:
            user = User.query.filter_by(id=userid).first()
            user.status = 'done'
            db.session.commit()
            return {'response': 'successfully'}
        except:
            return {'response': 'unsuccessfully'} 

DAO = TodoDAO()

@sm.route('/')
class TodoList(Resource):
    '''
        Shows a list of all todos, and lets you POST to add new tasks
    '''
    @sm.doc('list_todos')
    # @sm.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.get()

    @sm.doc('create_todo')
    @sm.expect(todo)
    # @sm.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(sm.payload), 201

@sm.route('/<int:id>')
@sm.response(404, 'Todo not found')
@sm.param('id', 'The task identifier')
class Todo(Resource):
    '''
        Show a single todo item and lets you delete them
    '''
    
    @sm.doc('get_todo')
    # @sm.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @sm.doc('delete_todo')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @sm.doc('update_todo')
    @sm.expect(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, sm.payload)

    @sm.doc('patch_todo')
    def patch(self, id):
        '''Patch a task given its identifier'''
        return DAO.patch(id), 200


if __name__ == "__main__":
    # app.run(debug=True)
    manager.run()