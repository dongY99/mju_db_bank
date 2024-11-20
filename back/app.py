from flask import Flask, jsonify
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@host/db_name'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # ...

class UserList(Resource):
    def get(self):
        users = User.query.all()
        return jsonify({'users': [user.to_json() for user in users]})

# ...

if __name__ == '__main__':
    app.run(debug=True)