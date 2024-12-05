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
                        "Date_Of_Birth": new_customer.Date_Of_Birth,
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
                        "Data_Of_Opening": Data_Of_Opening,
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
                        "Deposit_Account_ID": Deposit_Account_ID,
                        "Transaction_Amount": Transaction_Amount,
                        "Details_Of_Transaction": Details_Of_Transaction,
                        "Data_Of_Deposit_Withdrawal": Data_Of_Deposit_Withdrawal,
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
            Date_Of_Application=Date_Of_Application,
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
                        "Date_Of_Application": Date_Of_Application,
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
def query_accounts_by_name(name):
    query = (
        db.session.query(DepositAccount.Deposit_Account_ID, DepositAccount.Balance)
        .join(Customer)
        .filter(Customer.Name == name)
    )

    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    result = query.all()
    return result


def query_accounts_by_name_sorted(name):
    query = (
        db.session.query(
            DepositAccount.Deposit_Account_ID,
            DepositAccount.Balance,
            DepositAccount.Data_Of_Opening,
        )
        .join(Customer)
        .filter(Customer.Name == name)
        .order_by(DepositAccount.Data_Of_Opening.asc())
    )

    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    result = query.all()
    return result


def query_recent_transactions(name, account_id):
    one_month_ago = datetime.now() - timedelta(days=30)
    query = (
        db.session.query(
            Transaction.거래번호,
            Transaction.Data_Of_Deposit_Withdrawal,
            Transaction.Transaction_Amount,
            Transaction.Details_Of_Transaction,
        )
        .join(DepositAccount)
        .join(Customer)
        .filter(Customer.Name == name, DepositAccount.Deposit_Account_ID == account_id)
        .filter(Transaction.Data_Of_Deposit_Withdrawal >= one_month_ago)
        .order_by(Transaction.Data_Of_Deposit_Withdrawal.desc())
    )

    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    result = query.all()
    return result


def query_cards_by_name(name):
    query = (
        db.session.query(
            Card.Card_ID,
            Card.Card_Type,
            Card.Limit_Amount,
            DepositAccount.Deposit_Account_ID,
        )
        .join(Customer)
        .outerjoin(
            DepositAccount, Card.Deposit_Account_ID == DepositAccount.Deposit_Account_ID
        )
        .filter(Customer.Name == name)
    )

    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    result = query.all()
    return result


def query_next_birthday():
    today = datetime.now().date()
    query = (
        db.session.query(Customer.Name, Customer.Address, Customer.Date_Of_Birth)
        .filter(func.day(Customer.Date_Of_Birth) >= func.day(today))
        .order_by(
            func.day(Customer.Date_Of_Birth)
            - func.day(today)  # 생일이 가까운 순으로 정렬
        )
        .first()
    )

    # 쿼리 출력
    print(str(query.statement.compile(dialect=db.engine.dialect)))

    result = query.first()
    return result


def update_customer(Resident_Registration_Number):
    try:
        data = request.get_json()

        # 고객 조회
        customer = db.session.get(Customer, Resident_Registration_Number)
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        # 업데이트할 필드
        customer.Name = data.get("Name", customer.Name)
        customer.Address = data.get("Address", customer.Address)
        customer.Date_Of_Birth = data.get("Date_Of_Birth", customer.Date_Of_Birth)
        customer.Email = data.get("Email", customer.Email)
        customer.Phone_Number = data.get("Phone_Number", customer.Phone_Number)
        customer.Occupation = data.get("Occupation", customer.Occupation)

        # 데이터베이스 커밋
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Customer updated successfully",
                    "customer": {
                        "Resident_Registration_Number": customer.Resident_Registration_Number,
                        "Name": customer.Name,
                        "Address": customer.Address,
                        "Date_Of_Birth": customer.Date_Of_Birth,
                        "Email": customer.Email,
                        "Phone_Number": customer.Phone_Number,
                        "Occupation": customer.Occupation,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error updating customer", "details": str(e)}), 500


def update_deposit_account(Deposit_Account_ID):
    try:
        data = request.get_json()

        # 예금계좌 조회
        account = db.session.get(DepositAccount, Deposit_Account_ID)
        if not account:
            return jsonify({"error": "Deposit account not found"}), 404

        # 업데이트할 필드
        account.Account_Type = data.get("Account_Type", account.Account_Type)
        account.Balance = data.get("Balance", account.Balance)
        account.Card_Application_Status = data.get(
            "Card_Application_Status", account.Card_Application_Status
        )
        account.Data_Of_Opening = data.get("Data_Of_Opening", account.Data_Of_Opening)

        # 데이터베이스 커밋
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Deposit account updated successfully",
                    "deposit_account": {
                        "Deposit_Account_ID": account.Deposit_Account_ID,
                        "Account_Type": account.Account_Type,
                        "Balance": account.Balance,
                        "Card_Application_Status": account.Card_Application_Status,
                        "Data_Of_Opening": account.Data_Of_Opening,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"error": "Error updating deposit account", "details": str(e)}),
            500,
        )


def update_transaction(Transaction_Number):
    try:
        data = request.get_json()

        # 트랜잭션 조회
        transaction = db.session.get(Transaction, Transaction_Number)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        # 업데이트할 필드
        transaction.Data_Of_Deposit_Withdrawal = data.get(
            "Data_Of_Deposit_Withdrawal", transaction.Data_Of_Deposit_Withdrawal
        )
        transaction.Transaction_Amount = data.get(
            "Transaction_Amount", transaction.Transaction_Amount
        )
        transaction.Balance = data.get("Balance", transaction.Balance)
        transaction.Details_Of_Transaction = data.get(
            "Details_Of_Transaction", transaction.Details_Of_Transaction
        )

        # 데이터베이스 커밋
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Transaction updated successfully",
                    "transaction": {
                        "Transaction_Number": transaction.Transaction_Number,
                        "Data_Of_Deposit_Withdrawal": transaction.Data_Of_Deposit_Withdrawal,
                        "Transaction_Amount": transaction.Transaction_Amount,
                        "Balance": transaction.Balance,
                        "Details_Of_Transaction": transaction.Details_Of_Transaction,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error updating transaction", "details": str(e)}), 500


def update_card(Card_ID):
    try:
        data = request.get_json()

        # 카드 조회
        card = db.session.get(Card, Card_ID)
        if not card:
            return jsonify({"error": "Card not found"}), 404

        # 업데이트할 필드
        card.Date_Of_Application = data.get(
            "Date_Of_Application", card.Date_Of_Application
        )
        card.Limit_Amount = data.get("Limit_Amount", card.Limit_Amount)
        card.Payment_Date = data.get("Payment_Date", card.Payment_Date)
        card.Card_Type = data.get("Card_Type", card.Card_Type)

        # 데이터베이스 커밋
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Card updated successfully",
                    "card": {
                        "Card_ID": card.Card_ID,
                        "Date_Of_Application": card.Date_Of_Application,
                        "Limit_Amount": card.Limit_Amount,
                        "Payment_Date": card.Payment_Date,
                        "Card_Type": card.Card_Type,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error updating card", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
