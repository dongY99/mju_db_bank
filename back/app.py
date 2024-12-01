from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from models import db, Customer, DepositAccount, Transaction, Card
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func

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

#post, db 삽입
def add_customer():
    try:
        # 클라이언트로부터 JSON 데이터 받기
        data = request.get_json()

        # 필수 필드 값 추출
        주민번호 = data.get('주민번호')
        이름 = data.get('이름')
        생년월일 = data.get('생년월일')
        
        # 필수 필드가 없으면 오류 반환
        if not 주민번호 or not 이름 or not 생년월일:
            return jsonify({"error": "주민번호, 이름, 생년월일은 필수 항목입니다."}), 400

        # 이미 존재하는 고객인지 확인 (중복 삽입 방지)
        existing_customer = db.session.get(Customer, 주민번호)
        if existing_customer:
            return jsonify({"error": "이미 존재하는 주민번호입니다."}), 409

        # 새로운 고객 객체 생성
        new_customer = Customer(
            주민번호=주민번호,
            이름=이름,
            주소=data.get('주소', None),  # 선택적 필드
            생년월일=생년월일,
            이메일=data.get('이메일', None),
            전화번호=data.get('전화번호', None),
            직업=data.get('직업', None)
        )

        # 데이터베이스에 추가
        db.session.add(new_customer)
        db.session.commit()  # 커밋하여 데이터 저장

        # 성공 메시지 반환
        return jsonify({
            "message": "고객이 성공적으로 추가되었습니다.",
            "customer": {
                "주민번호": 주민번호,
                "이름": 이름,
                "주소": new_customer.주소,
                "생년월일": new_customer.생년월일,
                "이메일": new_customer.이메일,
                "전화번호": new_customer.전화번호,
                "직업": new_customer.직업
            }
        }), 201

    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "고객 추가 중 오류 발생", "details": str(e)}), 500

def add_deposit_account():
    try:
        # 클라이언트로부터 JSON 데이터 받기
        data = request.get_json()

        # 필수 필드 값 추출
        예금계좌ID = data.get('예금계좌ID')
        계좌종류 = data.get('계좌종류')
        잔고 = data.get('잔고', 0.0)  # 기본값 설정
        개설일자 = data.get('개설일자')
        고객주민번호 = data.get('고객주민번호')

        # 필수 필드가 없으면 오류 반환
        if not 예금계좌ID or not 계좌종류 or not 개설일자 or not 고객주민번호:
            return jsonify({"error": "예금계좌ID, 계좌종류, 개설일자, 고객주민번호는 필수 항목입니다."}), 400

        # 기존 고객 확인
        customer = db.session.get(Customer, 고객주민번호)
        if not customer:
            return jsonify({"error": "존재하지 않는 고객입니다."}), 404

        # 새로운 예금계좌 객체 생성
        new_account = DepositAccount(
            예금계좌ID=예금계좌ID,
            계좌종류=계좌종류,
            잔고=잔고,
            개설일자=개설일자,
            고객주민번호=고객주민번호
        )

        # 데이터베이스에 추가
        db.session.add(new_account)
        db.session.commit()  # 커밋하여 데이터 저장

        # 성공 메시지 반환
        return jsonify({
            "message": "예금계좌가 성공적으로 추가되었습니다.",
            "deposit_account": {
                "예금계좌ID": 예금계좌ID,
                "계좌종류": 계좌종류,
                "잔고": 잔고,
                "개설일자": 개설일자,
                "고객주민번호": 고객주민번호
            }
        }), 201

    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "예금계좌 추가 중 오류 발생", "details": str(e)}), 500

def add_transaction():
    try:
        # 클라이언트로부터 JSON 데이터 받기
        data = request.get_json()

        # 필수 필드 값 추출
        예금계좌ID = data.get('예금계좌ID')
        거래금액 = data.get('거래금액')
        거래내용 = data.get('거래내용', '')
        입출금날짜 = data.get('입출금날짜')

        # 필수 필드가 없으면 오류 반환
        if not 예금계좌ID or not 거래금액 or not 입출금날짜:
            return jsonify({"error": "예금계좌ID, 거래금액, 입출금날짜는 필수 항목입니다."}), 400

        # 예금계좌 존재 여부 확인
        deposit_account = db.session.get(DepositAccount, 예금계좌ID)
        if not deposit_account:
            return jsonify({"error": "존재하지 않는 예금계좌입니다."}), 404

        # 거래 금액에 따라 계좌 잔고 업데이트
        새로운잔고 = deposit_account.잔고 + 거래금액  # 입금(+) 또는 출금(-)
        
        if 새로운잔고 < 0:
            return jsonify({"error": "출금액이 계좌 잔고를 초과할 수 없습니다."}), 400
        
        deposit_account.잔고 = 새로운잔고

        # 트랜잭션 객체 생성
        new_transaction = Transaction(
            예금계좌ID=예금계좌ID,
            거래금액=거래금액,
            거래내용=거래내용,
            입출금날짜=입출금날짜,
            잔고=새로운잔고
        )

        # 트랜잭션과 예금계좌 업데이트
        db.session.add(new_transaction)
        db.session.commit()  # 커밋하여 트랜잭션 데이터 저장

        # 성공 메시지 반환
        return jsonify({
            "message": "트랜잭션이 성공적으로 추가되었습니다.",
            "transaction": {
                "예금계좌ID": 예금계좌ID,
                "거래금액": 거래금액,
                "거래내용": 거래내용,
                "입출금날짜": 입출금날짜,
                "잔고": 새로운잔고
            }
        }), 201

    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "트랜잭션 추가 중 오류 발생", "details": str(e)}), 500
    
def add_card():
    try:
        # 클라이언트로부터 JSON 데이터 받기
        data = request.get_json()

        # 필수 필드 값 추출
        카드ID = data.get('카드ID')
        카드종류 = data.get('카드종류')
        한도금액 = data.get('한도금액')
        결제일자 = data.get('결제일자')
        신청일자 = data.get('신청일자')
        고객주민번호 = data.get('고객주민번호')
        예금계좌ID = data.get('예금계좌ID', None)  # 선택적 필드

        # 필수 필드가 없으면 오류 반환
        if not 카드ID or not 카드종류 or not 한도금액 or not 결제일자 or not 신청일자 or not 고객주민번호:
            return jsonify({"error": "카드ID, 카드종류, 한도금액, 결제일자, 신청일자, 고객주민번호는 필수 항목입니다."}), 400

        # 기존 고객 확인
        customer = db.session.get(Customer, 고객주민번호)
        if not customer:
            return jsonify({"error": "존재하지 않는 고객입니다."}), 404

        # 예금계좌 확인 (선택적 필드)
        if 예금계좌ID:
            deposit_account = db.session.get(DepositAccount, 예금계좌ID)
            if not deposit_account:
                return jsonify({"error": "존재하지 않는 예금계좌입니다."}), 404
        else:
            deposit_account = None

        # 새로운 카드 객체 생성
        new_card = Card(
            카드ID=카드ID,
            카드종류=카드종류,
            한도금액=한도금액,
            결제일자=결제일자,
            신청일자=신청일자,
            고객주민번호=고객주민번호,
            예금계좌ID=예금계좌ID  # 예금계좌는 선택적
        )

        # 데이터베이스에 추가
        db.session.add(new_card)
        db.session.commit()  # 커밋하여 데이터 저장

        # 성공 메시지 반환
        return jsonify({
            "message": "카드가 성공적으로 추가되었습니다.",
            "card": {
                "카드ID": 카드ID,
                "카드종류": 카드종류,
                "한도금액": 한도금액,
                "결제일자": 결제일자,
                "신청일자": 신청일자,
                "고객주민번호": 고객주민번호,
                "예금계좌ID": 예금계좌ID
            }
        }), 201

    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "카드 추가 중 오류 발생", "details": str(e)}), 500
    
#쿼리
def query_accounts_by_name(name):
    query = (
        db.session.query(DepositAccount.예금계좌ID, DepositAccount.잔고)
        .join(Customer)
        .filter(Customer.이름 == name)
    )
    
    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))
    
    result = query.all()
    return result


def query_accounts_by_name_sorted(name):
    query = (
        db.session.query(DepositAccount.예금계좌ID, DepositAccount.잔고, DepositAccount.개설일자)
        .join(Customer)
        .filter(Customer.이름 == name)
        .order_by(DepositAccount.개설일자.asc())
    )
    
    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))
    
    result = query.all()
    return result


def query_recent_transactions(name, account_id):
    one_month_ago = datetime.now() - timedelta(days=30)
    query = (
        db.session.query(Transaction.거래번호, Transaction.입출금날짜, Transaction.거래금액, Transaction.거래내용)
        .join(DepositAccount)
        .join(Customer)
        .filter(Customer.이름 == name, DepositAccount.예금계좌ID == account_id)
        .filter(Transaction.입출금날짜 >= one_month_ago)
        .order_by(Transaction.입출금날짜.desc())
    )
    
    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))
    
    result = query.all()
    return result

def query_cards_by_name(name):
    query = (
        db.session.query(Card.카드ID, Card.카드종류, Card.한도금액, DepositAccount.예금계좌ID)
        .join(Customer)
        .outerjoin(DepositAccount, Card.예금계좌ID == DepositAccount.예금계좌ID)
        .filter(Customer.이름 == name)
    )
    
    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))
    
    result = query.all()
    return result

def query_next_birthday():
    today = datetime.now().date()
    query = (
        db.session.query(
            Customer.이름, Customer.주소, Customer.생년월일
        )
        .filter(func.day(Customer.생년월일) >= func.day(today))
        .order_by(
            func.day(Customer.생년월일) - func.day(today)  # 생일이 가까운 순으로 정렬
        )
        .first()
    )
    
    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))
    
    result = query.first()
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)