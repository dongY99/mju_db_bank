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
    static_folder=os.path.join("dist", "static"),  # Vue 정적 파일 경로
    template_folder=os.path.join("dist"),  # Vue 템플릿 경로
)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/mydb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/customers", methods=["GET"])
def getCutomers():
    try:
        customers = Customer.query.all()
        customer_list = [
            {
                "Resident_Registration_Number": c.Resident_Registration_Number,
                "Name": c.Name,
                "Address": c.Address,
                "Date_Of_Birth": (
                    c.Date_Of_Birth.strftime("%Y-%m-%d") if c.Date_Of_Birth else None
                ),
                "Email": c.Email,
                "Phone_Number": c.Phone_Number,
                "Occupation": c.Occupation,
            }
            for c in customers
        ]
        return jsonify(customer_list), 200
    except Exception as e:
        return jsonify({"error": "Error fetching customers", "details": str(e)}), 500


@app.route("/api/deposit_account", methods=["GET"])
def get_deposit_accounts():
    try:
        deposit_accounts = DepositAccount.query.all()
        account_list = [
            {
                "Deposit_Account_ID": account.Deposit_Account_ID,
                "Account_Type": account.Account_Type,
                "Balance": account.Balance,
                "Card_Application_Status": account.Card_Application_Status,
                "Data_Of_Opening": (
                    account.Data_Of_Opening.strftime("%Y-%m-%d")
                    if account.Data_Of_Opening
                    else None
                ),
                "Customer_Resident_Registration_Number": account.Customer_Resident_Registration_Number,
            }
            for account in deposit_accounts
        ]
        return jsonify(account_list), 200
    except Exception as e:
        return (
            jsonify({"error": "Error fetching deposit accounts", "details": str(e)}),
            500,
        )


@app.route("/api/card", methods=["GET"])
def get_cards():
    try:
        cards = Card.query.all()
        card_list = [
            {
                "Card_ID": card.Card_ID,
                "Date_Of_Application": (
                    card.Date_Of_Application.strftime("%Y-%m-%d")
                    if card.Date_Of_Application
                    else None
                ),
                "Limit_Amount": card.Limit_Amount,
                "Payment_Date": card.Payment_Date,
                "Card_Type": card.Card_Type,
                "Customer_Resident_Registration_Number": card.Customer_Resident_Registration_Number,
                "Deposit_Account_ID": card.Deposit_Account_ID,
            }
            for card in cards
        ]
        return jsonify(card_list), 200
    except Exception as e:
        return jsonify({"error": "Error fetching cards", "details": str(e)}), 500


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        transactions = Transaction.query.all()
        transaction_list = [{
            "Transaction_Number": transaction.Transaction_Number,
            "Deposit_Account_ID": transaction.Deposit_Account_ID,
            "Data_Of_Deposit_Withdrawal": transaction.Data_Of_Deposit_Withdrawal.strftime('%Y-%m-%d %H:%M:%S'),
            "Transaction_Amount": transaction.Transaction_Amount,
            "Balance": transaction.Balance,
            "Details_Of_Transaction": transaction.Details_Of_Transaction
        } for transaction in transactions]
        return jsonify(transaction_list), 200
    except Exception as e:
        return jsonify({"error": "Error fetching transactions", "details": str(e)}), 500


# post, db 삽입
@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        # 클라이언트로부터 JSON 데이터 받기
        data = request.get_json()

        # 필수 필드 값 추출
        Resident_Registration_Number = data.get("Resident_Registration_Number")
        Name = data.get("Name")
        Date_Of_Birth = data.get("Date_Of_Birth")

        # 필수 필드가 없으면 오류 반환
        if not Resident_Registration_Number or not Name or not Date_Of_Birth:
            return (
                jsonify({"error": "주민번호, 이름, 생년월일은 필수 항목입니다."}),
                400,
            )

        # 이미 존재하는 고객인지 확인 (중복 삽입 방지)
        existing_customer = db.session.get(Customer, Resident_Registration_Number)
        if existing_customer:
            return jsonify({"error": "이미 존재하는 주민번호입니다."}), 409

        # 새로운 고객 객체 생성
        new_customer = Customer(
            Resident_Registration_Number=Resident_Registration_Number,
            Name=Name,
            Address=data.get("Address", None),  # 선택적 필드
            Date_Of_Birth=Date_Of_Birth,
            Email=data.get("Email", None),
            Phone_Number=data.get("Phone_Number", None),
            Occupation=data.get("Occupation", None),
        )

        # 데이터베이스에 추가
        db.session.add(new_customer)
        db.session.commit()  # 커밋하여 데이터 저장

        # 성공 메시지 반환
        return (
            jsonify(
                {
                    "message": "고객이 성공적으로 추가되었습니다.",
                    "customer": {
                        "Resident_Registration_Number": Resident_Registration_Number,
                        "Name": Name,
                        "Address": new_customer.Address,
                        "Date_Of_Birth": new_customer.Date_Of_Birth.strftime("%Y-%m-%d") if new_customer.Date_Of_Birth else None,
                        "Email": new_customer.Email,
                        "Phone_Number": new_customer.Phone_Number,
                        "Occupation": new_customer.Occupation,
                    },
                }
            ),
            201,
        )

    except Exception as e:
        print(f"Error details: {str(e)}")
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "고객 추가 중 오류 발생", "details": str(e)}), 500

@app.route('/add_deposit_account', methods=['POST'])
def add_deposit_account():
    try:
        # 클라이언트로부터 JSON 데이터 받기
        data = request.get_json()


        # 필수 필드 값 추출
        Deposit_Account_ID = data.get("Deposit_Account_ID")
        Account_Type = data.get("Account_Type")
        Balance = data.get("Balance", 0.0)  # 기본값 설정
        Data_Of_Opening = data.get("Data_Of_Opening")
        Card_Application_Status = data.get("Card_Application_Status")
        Customer_Resident_Registration_Number = data.get(
            "Customer_Resident_Registration_Number"
        )

        # 필수 필드가 없으면 오류 반환
        if (
            not Deposit_Account_ID
            or not Account_Type
            or not Data_Of_Opening
            or not Customer_Resident_Registration_Number
        ):
            return (
                jsonify(
                    {
                        "error": "계좌ID, 계좌종류, 개설날짜, 고객주민번호는 필수 항목입니다."
                    }
                ),
                400,
            )

        # 기존 고객 확인
        customer = db.session.get(Customer, Customer_Resident_Registration_Number)
        if not customer:
            return jsonify({"error": "존재하지 않는 고객입니다."}), 404

        # 새로운 예금계좌 객체 생성
        new_account = DepositAccount(
            Deposit_Account_ID=Deposit_Account_ID,
            Account_Type=Account_Type,
            Balance=Balance,
            Data_Of_Opening=Data_Of_Opening,
            Card_Application_Status=Card_Application_Status,
            Customer_Resident_Registration_Number=Customer_Resident_Registration_Number,
        )

        # 데이터베이스에 추가
        db.session.add(new_account)
        db.session.commit()  # 커밋하여 데이터 저장

        # 성공 메시지 반환
        return (
            jsonify(
                {
                    "message": "예금계좌가 성공적으로 추가되었습니다.",
                    "deposit_account": {
                        "Deposit_Account_ID": Deposit_Account_ID,
                        "Account_Type": Account_Type,
                        "Balance": Balance,
                        "Data_Of_Opening": new_account.Data_Of_Opening.strftime("%Y-%m-%d"),
                        "Card_Application_Status": Card_Application_Status,
                        "Customer_Resident_Registration_Number": Customer_Resident_Registration_Number,
                    },
                }
            ),
            201,
        )

    except Exception as e:
        print(f"Error details: {str(e)}")
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "예금계좌 추가 중 오류 발생", "details": str(e)}), 500

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        # 클라이언트로부터 JSON 데이터 받기
        data = request.get_json()

        # 필수 필드 값 추출
        Deposit_Account_ID = data.get("Deposit_Account_ID")
        Transaction_Amount = data.get("Transaction_Amount")
        Details_Of_Transaction = data.get("Details_Of_Transaction", "")
        Data_Of_Deposit_Withdrawal = datetime.now()

        # 필수 필드가 없으면 오류 반환
        if (
            not Deposit_Account_ID
            or not Transaction_Amount
        ):
            return (
                jsonify({"error": "출금계좌, 거래금액는 필수 항목입니다."}),
                400,
            )

        # 예금계좌 존재 여부 확인
        deposit_account = db.session.get(DepositAccount, Deposit_Account_ID)
        if not deposit_account:
            return jsonify({"error": "존재하지 않는 예금계좌입니다."}), 404

        # 거래 금액에 따라 계좌 Balance 업데이트
        new_Balance = (
            deposit_account.Balance + Transaction_Amount
        )  # 입금(+) 또는 출금(-)

        if new_Balance < 0:
            return jsonify({"error": "출금액이 계좌 잔고를 초과할 수 없습니다."}), 400

        deposit_account.Balance = new_Balance
        
        # 트랜잭션 객체 생성
        new_transaction = Transaction(
            Deposit_Account_ID=Deposit_Account_ID,
            Transaction_Amount=Transaction_Amount,
            Details_Of_Transaction=Details_Of_Transaction,
            Data_Of_Deposit_Withdrawal=Data_Of_Deposit_Withdrawal,
            Balance=new_Balance,
        )

        # 트랜잭션과 예금계좌 업데이트
        db.session.add(new_transaction)
        db.session.commit()  # 커밋하여 트랜잭션 데이터 저장

        # 성공 메시지 반환
        return (
            jsonify(
                {
                    "message": "트랜잭션이 성공적으로 추가되었습니다.",
                    "transaction": {
                        "Transaction_Number": new_transaction.Transaction_Number,
                        "Deposit_Account_ID": Deposit_Account_ID,
                        "Transaction_Amount": Transaction_Amount,
                        "Details_Of_Transaction": Details_Of_Transaction,
                        "Data_Of_Deposit_Withdrawal": new_transaction.Data_Of_Deposit_Withdrawal.strftime('%Y-%m-%d %H:%M:%S'),
                        "Balance": new_Balance,
                    },
                }
            ),
            201,
        )

    except Exception as e:
        print(f"Error details: {str(e)}")
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "트랜잭션 추가 중 오류 발생", "details": str(e)}), 500

@app.route('/add_card', methods=['POST'])
def add_card():
    try:
        # 클라이언트로부터 JSON 데이터 받기
        data = request.get_json()
        print(data)

        # 필수 필드 값 추출
        Card_ID = data.get("Card_ID")
        Card_Type = data.get("Card_Type")
        Limit_Amount = data.get("Limit_Amount")
        Payment_Date = data.get("Payment_Date")
        Date_Of_Application = data.get("Date_Of_Application")
        Customer_Resident_Registration_Number = data.get(
            "Customer_Resident_Registration_Number"
        )
        Deposit_Account_ID = data.get("Deposit_Account_ID")

        # 필수 필드가 없으면 오류 반환
        if (
            not Card_ID
            or not Card_Type
            or not Limit_Amount
            or not Payment_Date
            or not Date_Of_Application
            or not Customer_Resident_Registration_Number
            or not Deposit_Account_ID
        ):
            return (
                jsonify(
                    {
                        "error": "카드ID, 카드종류, 한도금액, 결제날짜, 신청일자, 고객주민번호는 필수 항목입니다."
                    }
                ),
                400,
            )

        # 기존 고객 확인
        customer = db.session.get(Customer, Customer_Resident_Registration_Number)
        if not customer:
            return jsonify({"error": "존재하지 않는 고객입니다."}), 404

        # 예금계좌 확인
        deposit_account = db.session.get(DepositAccount, Deposit_Account_ID)
        if not deposit_account:
            return jsonify({"error": "존재하지 않는 예금계좌입니다."}), 404

        # 새로운 카드 객체 생성
        new_card = Card(
            Card_ID=Card_ID,
            Card_Type=Card_Type,
            Limit_Amount=Limit_Amount,
            Payment_Date=Payment_Date,
            Date_Of_Application=Date_Of_Application.strftime("%Y-%m-%d"),
            Customer_Resident_Registration_Number=Customer_Resident_Registration_Number,
            Deposit_Account_ID=Deposit_Account_ID,
        )

        # 데이터베이스에 추가
        db.session.add(new_card)
        db.session.commit()  # 커밋하여 데이터 저장

        # 성공 메시지 반환
        return (
            jsonify(
                {
                    "message": "카드가 성공적으로 추가되었습니다.",
                    "card": {
                        "Card_ID": Card_ID,
                        "Card_Type": Card_Type,
                        "Limit_Amount": Limit_Amount,
                        "Payment_Date": Payment_Date,
                        "Date_Of_Application": Date_Of_Application.strftime("%Y-%m-%d"),
                        "Customer_Resident_Registration_Number": Customer_Resident_Registration_Number,
                        "Deposit_Account_ID": Deposit_Account_ID,
                    },
                }
            ),
            201,
        )

    except Exception as e:
        print(f"Error details: {str(e)}")
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "카드 추가 중 오류 발생", "details": str(e)}), 500


# 쿼리
@app.route('/query/customer/pk', methods=['GET'])
def query_customer_by_pk():
    resident_registration_number = request.args.get('resident_registration_number')
    query = db.session.query(Customer).filter(Customer.Resident_Registration_Number == resident_registration_number)
    
    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    result = query.one_or_none()  # 결과가 없으면 None, 있으면 단일 객체 반환
    if result == None:
        return jsonify({"customer": []})
    else:
        return (
            jsonify(
                {
                    "message": "쿼리 성공.",
                    "customer": [{
                        "Resident_Registration_Number": result.Resident_Registration_Number,
                        "Name": result.Name,
                        "Address": result.Address,
                        "Date_Of_Birth": result.Date_Of_Birth.strftime("%Y-%m-%d") if result.Date_Of_Birth else None,
                        "Email": result.Email,
                        "Phone_Number": result.Phone_Number,
                        "Occupation": result.Occupation,
                    }],
                }
            ),
            201,
        )

@app.route('/query/deposit_account/pk', methods=['GET'])
def query_deposit_account_by_pk():
    deposit_account_id = request.args.get('deposit_account_id')
    query = db.session.query(DepositAccount).filter(DepositAccount.Deposit_Account_ID == deposit_account_id)
    
    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    result = query.one_or_none()  # 결과가 없으면 None 반환
    if result == None:
        return jsonify({"deposit_account": []})
    else:
        return (
            jsonify(
                {
                    "message": "쿼리 성공.",
                    "deposit_account": [{
                        "Deposit_Account_ID": result.Deposit_Account_ID,
                        "Account_Type": result.Account_Type,
                        "Balance": result.Balance,
                        "Data_Of_Opening": result.Data_Of_Opening.strftime("%Y-%m-%d"),
                        "Card_Application_Status": result.Card_Application_Status,
                        "Customer_Resident_Registration_Number": result.Customer_Resident_Registration_Number,
                    }],
                }
            ),
            201,
        )

@app.route('/query/card/pk', methods=['GET'])
def query_card_by_pk():
    card_id = request.args.get('card_id')
    query = db.session.query(Card).filter(Card.Card_ID == card_id)
    
    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    result = query.one_or_none()  # 결과가 없으면 None 반환
    if result == None:
        return jsonify({"card": []})
    else:
        return (
            jsonify(
                {
                    "message": "쿼리 성공.",
                    "card": [{
                        "Card_ID": result.Card_ID,
                        "Card_Type": result.Card_Type,
                        "Limit_Amount": result.Limit_Amount,
                        "Payment_Date": result.Payment_Date,
                        "Date_Of_Application": result.Date_Of_Application.strftime("%Y-%m-%d"),
                        "Customer_Resident_Registration_Number": result.Customer_Resident_Registration_Number,
                        "Deposit_Account_ID": result.Deposit_Account_ID,
                    }],
                }
            ),
            201,
        )
    
@app.route('/query/transaction', methods=['GET'])
def query_transaction():
    deposit_account_id = request.args.get('deposit_account_id')
    query = db.session.query(Transaction).filter(Transaction.Deposit_Account_ID == deposit_account_id)
    
    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    result = query.all()
    if result == None:
        return jsonify({"transactions": []})
    else:
        return (
            jsonify(
                {
                    "message": "쿼리 성공.",
                    "transactions": [{
                        "Transaction_Number": transaction.Transaction_Number,
                        "Deposit_Account_ID": transaction.Deposit_Account_ID,
                        "Transaction_Amount": transaction.Transaction_Amount,
                        "Details_Of_Transaction": transaction.Details_Of_Transaction,
                        "Data_Of_Deposit_Withdrawal": transaction.Data_Of_Deposit_Withdrawal.strftime('%Y-%m-%d %H:%M:%S'),
                        "Balance": transaction.Balance,
                    } for transaction in result ],
                }
            ),
            201,
        )

@app.route('/query/customers/sorted', methods=['GET'])
def query_customers_sorted():
    # 정렬 기준 및 방향 받기
    sort_field = request.args.get('field', 'Name')  # 기본 필드는 Name
    sort_order = request.args.get('order', 'asc')  # 기본 정렬은 오름차순
    resident_registration_number = request.args.get('resident_registration_number')

    query = db.session.query(Customer).filter(Customer.Resident_Registration_Number == resident_registration_number)

    # 지원하는 정렬 필드와 유효성 검사
    valid_fields = ['Name', 'Address']
    if sort_field not in valid_fields:
        return jsonify({"error": "Invalid sort field. Allowed fields are 'Name' or 'Address'"}), 400

    # 정렬 방향 설정
    if sort_order == 'desc':
        order_clause = db.desc(getattr(Customer, sort_field))
    elif sort_order == 'asc':
        order_clause = getattr(Customer, sort_field)
    else:
        return jsonify({"error": "Invalid sort order. Allowed orders are 'asc' or 'desc'"}), 400
    print(sort_order)

    # 쿼리 생성
    if resident_registration_number:
        query = db.session.query(Customer).filter(Customer.Resident_Registration_Number == resident_registration_number).order_by(order_clause)
    else:
        query = db.session.query(Customer).order_by(order_clause)

    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    # 결과 실행
    result = query.all()

    # 결과 반환
    return (
        jsonify({
            "message": "쿼리 성공.",
            "customers": [{
                "Resident_Registration_Number": customer.Resident_Registration_Number,
                "Name": customer.Name,
                "Address": customer.Address,
                "Date_Of_Birth": customer.Date_Of_Birth.strftime("%Y-%m-%d") if customer.Date_Of_Birth else None,
                "Email": customer.Email,
                "Phone_Number": customer.Phone_Number,
                "Occupation": customer.Occupation,
            } for customer in result]
        }),
        200,
    )

@app.route('/query/deposit_accounts/sorted', methods=['GET'])
def query_deposit_accounts_sorted():
    # 정렬 기준 및 방향 받기
    sort_field = request.args.get('field', 'Account_Type')  # 기본 필드는 Account_Type
    sort_order = request.args.get('order', 'asc')          # 기본 정렬은 오름차순
    deposit_account_id = request.args.get('deposit_account_id')

    # 지원하는 정렬 필드와 유효성 검사
    valid_fields = ['Account_Type', 'Balance', 'Data_Of_Opening']
    if sort_field not in valid_fields:
        return jsonify({"error": f"Invalid sort field. Allowed fields are {', '.join(valid_fields)}"}), 400

    # 정렬 방향 설정
    if sort_order == 'desc':
        order_clause = db.desc(getattr(DepositAccount, sort_field))
    elif sort_order == 'asc':
        order_clause = getattr(DepositAccount, sort_field)
    else:
        return jsonify({"error": "Invalid sort order. Allowed orders are 'asc' or 'desc'"}), 400

    # 쿼리 생성
    if deposit_account_id:
        query = db.session.query(DepositAccount).filter(DepositAccount.Deposit_Account_ID == deposit_account_id).order_by(order_clause)
    else:
        query = db.session.query(DepositAccount).order_by(order_clause)

    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    # 결과 실행
    result = query.all()

    # 결과 반환
    return (
        jsonify({
            "message": "쿼리 성공.",
            "deposit_accounts": [{
                "Deposit_Account_ID": account.Deposit_Account_ID,
                "Account_Type": account.Account_Type,
                "Balance": account.Balance,
                "Data_Of_Opening": account.Data_Of_Opening.strftime("%Y-%m-%d"),
                "Card_Application_Status": account.Card_Application_Status,
                "Customer_Resident_Registration_Number": account.Customer_Resident_Registration_Number,
            } for account in result]
        }),
        200,
    )

@app.route('/query/transactions/sorted', methods=['GET'])
def query_transactions_sorted():
    # 정렬 기준 및 방향 받기
    sort_field = request.args.get('field', 'Data_Of_Deposit_Withdrawal')  # 기본 필드는 Data_Of_Deposit_Withdrawal
    sort_order = request.args.get('order', 'asc')                        # 기본 정렬은 오름차순
    deposit_account_id = request.args.get('deposit_account_id')
    print(deposit_account_id)
    
    # 지원하는 정렬 필드와 유효성 검사
    valid_fields = ['Data_Of_Deposit_Withdrawal']
    if sort_field not in valid_fields:
        return jsonify({"error": f"Invalid sort field. Allowed fields are {', '.join(valid_fields)}"}), 400

    # 정렬 방향 설정
    if sort_order == 'desc':
        order_clause = db.desc(getattr(Transaction, sort_field))
    elif sort_order == 'asc':
        order_clause = getattr(Transaction, sort_field)
    else:
        return jsonify({"error": "Invalid sort order. Allowed orders are 'asc' or 'desc'"}), 400

    # 쿼리 생성
    if deposit_account_id:
        query = db.session.query(Transaction).filter(Transaction.Deposit_Account_ID == deposit_account_id).order_by(order_clause)
    else:
        query = db.session.query(Transaction).order_by(order_clause)

    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    # 결과 실행
    result = query.all()

    # 결과 반환
    return (
        jsonify({
            "message": "쿼리 성공.",
            "transactions": [{
                "Transaction_Number": transaction.Transaction_Number,
                "Deposit_Account_ID": transaction.Deposit_Account_ID,
                "Data_Of_Deposit_Withdrawal": transaction.Data_Of_Deposit_Withdrawal.strftime('%Y-%m-%d %H:%M:%S'),
                "Transaction_Amount": transaction.Transaction_Amount,
                "Balance": transaction.Balance,
                "Details_Of_Transaction": transaction.Details_Of_Transaction,
            } for transaction in result]
        }),
        200,
    )

@app.route('/query/cards/sorted', methods=['GET'])
def query_cards_sorted():
    # 정렬 기준 및 방향 받기
    sort_field = request.args.get('field', 'Date_Of_Application')  # 기본 필드는 Date_Of_Application
    sort_order = request.args.get('order', 'asc')                 # 기본 정렬은 오름차순
    card_id = request.args.get('card_id')

    # 지원하는 정렬 필드와 유효성 검사
    valid_fields = ['Date_Of_Application', 'Card_Type', 'Limit_Amount']
    if sort_field not in valid_fields:
        return jsonify({"error": f"Invalid sort field. Allowed fields are {', '.join(valid_fields)}"}), 400

    # 정렬 방향 설정
    if sort_order == 'desc':
        order_clause = db.desc(getattr(Card, sort_field))
    elif sort_order == 'asc':
        order_clause = getattr(Card, sort_field)
    else:
        return jsonify({"error": "Invalid sort order. Allowed orders are 'asc' or 'desc'"}), 400

    # 쿼리 생성
    if card_id:
        query = db.session.query(Card).filter(Card.Card_ID == card_id).order_by(order_clause)
    else:
        query = db.session.query(Card).order_by(order_clause)

    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    # 결과 실행
    result = query.all()

    # 결과 반환
    return (
        jsonify({
            "message": "쿼리 성공.",
            "cards": [{
                "Card_ID": card.Card_ID,
                "Card_Type": card.Card_Type,
                "Limit_Amount": card.Limit_Amount,
                "Payment_Date": card.Payment_Date,
                "Date_Of_Application": card.Date_Of_Application.strftime("%Y-%m-%d"),
                "Customer_Resident_Registration_Number": card.Customer_Resident_Registration_Number,
                "Deposit_Account_ID": card.Deposit_Account_ID,
            } for card in result]
        }),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
