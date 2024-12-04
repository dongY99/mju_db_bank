from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    Resident_Registration_Number = db.Column(db.String(14), primary_key=True)  # Resident_Registration_Number는 PK
    Name = db.Column(db.String(50), nullable=False)
    Address = db.Column(db.String(255), nullable=True)
    Date_Of_Birth = db.Column(db.Date, nullable=False)
    Email = db.Column(db.String(100), nullable=True)
    Phone_Number = db.Column(db.String(15), nullable=True)
    Occupation = db.Column(db.String(50), nullable=True)

    # Relationship
    deposit_accounts = db.relationship('DepositAccount', backref='customer', lazy=True)
    cards = db.relationship('Card', backref='customer', lazy=True)


class DepositAccount(db.Model):
    __tablename__ = 'deposit_accounts'
    Deposit_Account_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Account_Type = db.Column(db.String(50), nullable=False)
    Balance = db.Column(db.Float, nullable=False)
    Card_Application_Status = db.Column(db.Boolean, default=False)
    Data_Of_Opening = db.Column(db.Date, nullable=False)
    Customer_Resident_Registration_Number = db.Column(db.String(14), db.ForeignKey('customers.Resident_Registration_Number'), nullable=False)

    # Relationship
    transactions = db.relationship('Transaction', backref='deposit_account', lazy=True)
    card = db.relationship('Card', backref='deposit_account', uselist=False)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    Transaction_Number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Deposit_Account_ID = db.Column(db.Integer, db.ForeignKey('deposit_accounts.Deposit_Account_ID'), nullable=False)
    Data_Of_Deposit_Withdrawal = db.Column(db.DateTime, nullable=False)
    Transaction_Amount = db.Column(db.Float, nullable=False)
    Balance = db.Column(db.Float, nullable=False)
    Details_Of_Transaction = db.Column(db.String(255), nullable=True)


class Card(db.Model):
    __tablename__ = 'cards'
    Card_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Date_Of_Application = db.Column(db.Date, nullable=False)
    Limit_Amount = db.Column(db.Float, nullable=False)
    Payment_Date = db.Column(db.Date, nullable=False)
    Card_Type = db.Column(db.String(50), nullable=False)
    Customer_Resident_Registration_Number = db.Column(db.String(14), db.ForeignKey('customers.Resident_Registration_Number'), nullable=False)
    Deposit_Account_ID = db.Column(db.Integer, db.ForeignKey('deposit_accounts.Deposit_Account_ID'), nullable=False)
