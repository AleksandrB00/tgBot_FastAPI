import datetime
import pydantic_models
import bit
from db import *
import random


@db_session
def create_wallet(user: pydantic_models.User = None, private_key: str = None, testnet: bool = False):
    if not testnet: 
        raw_wallet = bit.Key() if not private_key else bit.Key(private_key)
    else:
        raw_wallet = bit.PrivateKeyTestnet() if not private_key else bit.PrivateKeyTestnet(private_key)
    if user:
        wallet = Wallet(user=user, private_key=raw_wallet.to_wif(), address=raw_wallet.address)
    else:
        wallet = Wallet(private_key=raw_wallet.to_wif(), address=raw_wallet.address)
    flush()
    return wallet


@db_session
def create_user(tg_id: int, nick: str = None):
    if nick:
        user = User(tg_ID=tg_id, nick=nick, create_date=datetime.now(), wallet=create_wallet())
    else:
        user = User(tg_ID=tg_id, create_date=datetime.now(), wallet=create_wallet())
    flush()  
    return user

@db_session
def create_transaction(
    sender: User,
    amount_btc_without_fee: float,
    receiver: str,
    fee: float | None = None,
):
    
    if not fee:
        fee = amount_btc_without_fee * 15 / 100      
    amount_btc_with_fee = amount_btc_without_fee + fee  
    if amount_btc_without_fee + fee >= sender.wallet.balance:
        return f"Too low balance: {sender.wallet.balance}"
    
    sender.wallet.balance -= (amount_btc_without_fee + fee)
    receiver.wallet.balance += amount_btc_without_fee

    transaction = Transaction(sender=sender,
                              sender_wallet=sender.wallet,
                              fee=fee,
                              sender_address=sender.wallet.address,
                              receiver=receiver,
                              receiver_address=receiver.wallet.address,
                              recelver_wallet=receiver.wallet,
                              amount_btc_with_fee=amount_btc_with_fee,
                              amount_btc_without_fee=amount_btc_without_fee,
                              date_of_transaction=datetime.now(),
                              tx_hash=str(random.randint(1000000,9000000)))
    return transaction 

@db_session
def update_wallet_balance(wallet : pydantic_models.Wallet):
    return wallet.balance

@db_session
def update_all_wallet_balance():
    balance = []
    for wallet in select(i for i in Wallet)[:]:
        balance.append(wallet.balance)
    return ' '.join(str(balance))

@db_session
def get_user_by_id(id : int):
    return User[id]

@db_session
def get_user_by_tg_id(tg_id : str):
    return User.select(lambda u: u.tg_ID == tg_id).first()

@db_session
def get_transaction_info(transaction : pydantic_models.Transaction):
    return {
        'id' : transaction.id,
        'sender' : transaction.sender,
        'receiver' : transaction.receiver,
        'sender_wallet' : transaction.sender_wallet,
        'receiver_wallet' : transaction.recelver_wallet,
        'sender_address' : transaction.sender_address,
        'receiver_address' : transaction.receiver_address,
        'amount_btc_with_fee' : transaction.amount_btc_with_fee,
        'amount_btc_without_fee' : transaction.amount_btc_without_fee,
        'fee' : transaction.fee,
        'date_of_transaction' : transaction.date_of_transaction,
        'tx_hash' : transaction.tx_hash,
    }

@db_session
def get_wallet_info(wallet : pydantic_models.Wallet):
    return {
        'id' : wallet.id,
        'owner' : wallet.user.tg_ID,
        'balance' : wallet.balance,
    }

@db_session
def get_user_info(tg_id : pydantic_models.User):
    user = User.select(lambda u: u.tg_ID == tg_id).first()
    return {
        'id' : user.id,
        'tg_ID' : user.tg_ID,
        'nick' : user.nick if user.nick else None,
        'create_date' : user.create_date,
        'wallet' : get_wallet_info(user.wallet),
        'sended_transactions' : [trans.receiver.tg_ID for trans in Transaction.select(lambda u: u.sender == user)],
        'received_transactions' : [trans.sender.tg_ID for trans in Transaction.select(lambda u: u.receiver == user)],
    }
    
@db_session
def update_user(user: pydantic_models.User):
    user_to_update = User[user.id]
    if user.tg_ID:
        user_to_update.tg_ID = user.tg_ID
    if user.nick:
        user_to_update.nick = user.nick
    if user.create_date:
        user_to_update.create_date = user.create_date
    if user.wallet:
        user_to_update.wallet = user.wallet
    return user_to_update

@db_session
def get_balance(tg_ID:  pydantic_models.User):
    user = User.select(lambda u: u.tg_ID == tg_ID).first()
    return {
        'balance' : user.wallet.balance
    }

'''try:
    with db_session:
        print(get_user_info('@TestUser'))
except Exception as Ex:
    print(Ex)'''