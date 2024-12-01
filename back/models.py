from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    주민번호 = db.Column(db.String(13), primary_key=True)  # 주민번호는 PK
    이름 = db.Column(db.String(50), nullable=False)
    주소 = db.Column(db.String(255), nullable=True)
    생년월일 = db.Column(db.Date, nullable=False)
    이메일 = db.Column(db.String(100), nullable=True)
    전화번호 = db.Column(db.String(15), nullable=True)
    직업 = db.Column(db.String(50), nullable=True)

    # Relationship
    deposit_accounts = db.relationship('DepositAccount', backref='customer', lazy=True)
    cards = db.relationship('Card', backref='customer', lazy=True)


class DepositAccount(db.Model):
    __tablename__ = 'deposit_accounts'
    예금계좌ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    계좌종류 = db.Column(db.String(50), nullable=False)
    잔고 = db.Column(db.Float, nullable=False)
    카드신청여부 = db.Column(db.Boolean, default=False)
    개설일자 = db.Column(db.Date, nullable=False)
    고객주민번호 = db.Column(db.String(13), db.ForeignKey('customers.주민번호'), nullable=False)

    # Relationship
    transactions = db.relationship('Transaction', backref='deposit_account', lazy=True)
    card = db.relationship('Card', backref='deposit_account', uselist=False)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    거래번호 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    예금계좌ID = db.Column(db.Integer, db.ForeignKey('deposit_accounts.예금계좌ID'), nullable=False)
    입출금날짜 = db.Column(db.DateTime, nullable=False)
    거래금액 = db.Column(db.Float, nullable=False)
    잔고 = db.Column(db.Float, nullable=False)
    거래내용 = db.Column(db.String(255), nullable=True)


class Card(db.Model):
    __tablename__ = 'cards'
    카드ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    신청일자 = db.Column(db.Date, nullable=False)
    한도금액 = db.Column(db.Float, nullable=False)
    결제일자 = db.Column(db.Date, nullable=False)
    카드종류 = db.Column(db.String(50), nullable=False)
    고객주민번호 = db.Column(db.String(13), db.ForeignKey('customers.주민번호'), nullable=False)
    예금계좌ID = db.Column(db.Integer, db.ForeignKey('deposit_accounts.예금계좌ID'), nullable=True)
