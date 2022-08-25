from pony.orm import *
from datetime import datetime


db = Database()

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    tg_ID = Required(str, unique=True)
    nick = Optional(str)
    create_date = Required(datetime)
    wallet = Required('Wallet')
    sended_transactions = Set('Transaction', reverse='sender')
    recelved_transacyions = Set('Transaction', reverse='receiver')


class Wallet(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Optional(User)
    balance = Required(float, default="0.0")
    private_key = Required(str, unique=True)
    address = Required(str, unique=True)
    recelved_transaction = Set('Transaction', reverse='recelver_wallet')
    sender_transactions = Set('Transaction', reverse='sender_wallet')


class Transaction(db.Entity):
    id = PrimaryKey(int, auto=True)
    sender = Optional(User, reverse='sended_transactions')
    receiver = Optional(User, reverse='recelved_transacyions')
    recelver_wallet = Optional(Wallet, reverse='recelved_transaction')
    sender_wallet = Optional(Wallet, reverse='sender_transactions')
    sender_address = Optional(str)
    receiver_address = Optional(str)
    amount_btc_with_fee = Required(float)
    amount_btc_without_fee = Required(float)
    fee = Required(float)
    date_of_transaction = Required(datetime)
    tx_hash = Required(str, unique=True)