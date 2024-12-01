from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from models import db, Customer, DepositAccount, Transaction, Card
import datetime

app = Flask(
    __name__,
    static_folder=os.path.join('dist', 'static'),  # Vue 정적 파일 경로
    template_folder=os.path.join('dist')           # Vue 템플릿 경로
)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return {"message": "Hello from Flask!"}

@app.route('/world')
def world():
    customers = Customer.query.all()
    return jsonify([{
        "주민번호": c.주민번호,
        "이름": c.이름,
        "주소": c.주소,
        "생년월일": c.생년월일.strftime('%Y-%m-%d') if c.생년월일 else None,
        "이메일": c.이메일,
        "전화번호": c.전화번호,
        "직업": c.직업
    } for c in customers])

@app.route('/my')
def my():
    birth_date = datetime.date(1999, 1, 1)
    formatted_date = birth_date.strftime("%Y-%m-%d")
    try:
        # 데이터 검증
        주민번호 = '123'
        이름 = 'lee'
        주소 = 'magok'
        생년월일 = formatted_date
        이메일 = 'hanmeot'
        전화번호 = '456'
        직업 = 'student'

        if not 주민번호 or not 이름 or not 생년월일:
            return jsonify({"error": "주민번호, 이름, 생년월일은 필수 항목입니다."}), 400

        # 기존 고객 확인
        existing_customer = db.session.get(Customer, 주민번호)
        if existing_customer:
            return jsonify({"error": "이미 존재하는 주민번호입니다."}), 409

        # 새 고객 객체 생성
        new_customer = Customer(
            주민번호=주민번호,
            이름=이름,
            주소=주소,
            생년월일=생년월일,
            이메일=이메일,
            전화번호=전화번호,
            직업=직업
        )

        # 데이터베이스에 저장
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"message": "고객 추가 완료", "customer": {
            "주민번호": 주민번호,
            "이름": 이름,
            "주소": 주소,
            "생년월일": 생년월일,
            "이메일": 이메일,
            "전화번호": 전화번호,
            "직업": 직업
        }}), 201

    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "고객 추가 중 오류 발생", "details": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)