from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os


app = Flask(
    __name__,
    static_folder=os.path.join('dist', 'static'),  # Vue 정적 파일 경로
    template_folder=os.path.join('dist')           # Vue 템플릿 경로
)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@host/db_name'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)

# class UserList(Resource):
#     def get(self):
#         users = User.query.all()
#         return jsonify({'users': [user.to_json() for user in users]})

# API 엔드포인트 예시
@app.route('/api/hello')
def hello():
    return {"message": "Hello from Flask!"}

# Vue의 index.html 서빙
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and path.startswith('static/'):
        # 정적 파일 요청 처리
        return app.send_static_file(path)
    else:
        # Vue의 index.html 반환
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)