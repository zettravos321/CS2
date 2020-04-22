from flask_restful import Resource, Api
from flask import Flask, Response, json, jsonify, request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/kampus'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/admin')
def admin_page():
    return 'Halaman Admin'

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/HelloWorld')

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True)

    email = db.Column(db.String(120), unique=True)



    def __init__(self, username, email):

        self.username = username

        self.email = email


    @staticmethod

    def get_all_users():

        return User.query.all()


class UserSchema(ma.Schema):

    class Meta:

        # Fields to expose

        fields = ('id', 'username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/user/", methods=["GET"])

def get_user():
    all_users = User.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result)
@app.route("/user/<int:id>/", methods=["GET"])

def one_user(id):

    user = User.query.get(id)

    result = user_schema.dump(user)

    return jsonify(result)





@app.route("/user/", methods=["POST"])

def create_user():

    if not request.json or not 'username ' in request.json and not 'email' in request.json:

        abort(400)



    user = User(request.json['username'], request.json['email'])

    db.session.add(user)

    db.session.commit()



    result = user_schema.dump(user)

    return jsonify(result)





@app.route("/user/<int:id>/", methods=["PUT"])

def update_user(id):

    if not request.json or not 'username' in request.json and not 'email' in request.json:

        abort(400)



    user = User.query.get(id)

    user.username = request.json['username']

    user.email = request.json['email']

    db.session.commit()



    result = user_schema.dump(user)

    return jsonify(result)




@app.route("/user/<int:id>/", methods=["DELETE"])

def delete_user(id):

    user = User.query.get(id)

    db.session.delete(user)

    db.session.commit()



    return jsonify()


if __name__ == '__main__':
    app.run()
