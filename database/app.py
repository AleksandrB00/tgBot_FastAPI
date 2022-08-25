import fastapi
from fastapi import Request
import pydantic_models
import crud


api = fastapi.FastAPI()

@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.User_to_update = fastapi.Body()):
    return crud.update_user(user).to_dict()

@api.delete('/user/{user_id}')
@crud.db_session
def delete_user(user_id : int = fastapi.Path()):
    crud.get_user_by_id(user_id).dalete()
    return True

@api.post('/user/create')
def create_user(user: pydantic_models.User_to_create):
    return crud.create_user(
        tg_id=user.tg_ID,
        nick=user.nick if user.nick else None).to_dict()

@api.get('/get_info_by_user_id/{tg_ID}')
@crud.db_session
def get_info_by_user_tg(tg_ID: str = fastapi.Path()):
    return crud.get_user_info(tg_ID)

@api.get('/get_user_balance/{tg_ID}')
@crud.db_session
def get_user_balance(tg_ID: str = fastapi.Path()):
    return crud.get_balance(tg_ID)

@api.get('/get_total_balance')
@crud.db_session
def get_total_balance():
    balance = 0.0
    crud.update_all_wallet_balance()
    for user in crud.User.select()[:]:
        balance += user.wallet.balance
    return balance

@api.get("/users")
@crud.db_session
def get_users():
    users = []
    for user in crud.User.select()[:]:
        users.append(user.to_dict())
    return users

@api.post('/create_transaction')
@crud.db_session
def create_transaction(sender: str = fastapi.Body(), receiver: str = fastapi.Body(), amount_btc_without_fee: float = fastapi.Body()):
    user_sender = crud.get_user_by_tg_id(sender)
    user_receiver = crud.get_user_by_tg_id(receiver)
    return crud.create_transaction(user_sender, amount_btc_without_fee, user_receiver)