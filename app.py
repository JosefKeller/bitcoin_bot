import uvicorn
import fastapi
from fastapi import FastAPI

import pydantic_models
from database import crud

api = FastAPI()


@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.UserToUpdate = fastapi.Body()):
    if user_id == user.id:
        return crud.update_user(user).to_dict()


@api.delete('/user/{user_id}')
@crud.db_session
def delete_user(user_id: int = fastapi.Path()):
    crud.get_user_by_id(user_id).delete()
    return True


@api.post('/user/create')
def create_user(user: pydantic_models.UserToCreate):
    return crud.create_user(tg_id=user.tg_ID,
                            nick=user.nick if user.nick else None).to_dict()


@api.get('/get_info_by_user_id/{user_id:int}')
@crud.db_session
def get_info_about_user(user_id):
    return crud.get_user_info(crud.User[user_id])


@api.get('/get_user_balance_by_id/{user_id:int}')
@crud.db_session
def get_user_balance_by_id(user_id):
    crud.update_wallet_balance(crud.User[user_id].wallet)
    return crud.User[user_id].wallet.balance


@api.get('/get_total_balance')
@crud.db_session
def get_total_balance():
    balance = 0.0
    crud.update_all_wallets()
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


@api.get("/user_by_tg_id/{tg_id:int}")
@crud.db_session
def get_user_by_tg_id(tg_id):
    user = crud.get_user_info(crud.User.get(tg_ID=tg_id))
    return user


@api.get("/wallets")
@crud.db_session
def get_wallets():
    wallets = []
    for wallet in crud.Wallet.select()[:]:
        wallets.append(wallet.to_dict())
    return wallets


@api.get("/get_user_wallet/{user_id:int}")
@crud.db_session
def get_user_wallet(user_id):
    return crud.get_wallet_info(crud.User[user_id].wallet)


@api.get("/transactions")
@crud.db_session
def get_transactions():
    transactions = []
    for transaction in crud.Transaction.select()[:]:
        transactions.append(transaction.to_dict())
    return transactions


@api.post("/user/{tg_id}/create_transaction")
@crud.db_session
def create_transaction(tg_id: int = fastapi.Path(),
                       transaction: pydantic_models.TransactionToCreate = fastapi.Body()):
    user = crud.get_user_by_tg_id(tg_id)
    try:
        return crud.create_transaction(user,
                                       transaction.amount_btc_without_fee, transaction.receiver_address).to_dict()
    except AttributeError:
        return crud.create_transaction(user,
                                       transaction.amount_btc_without_fee, transaction.receiver_address)


@api.get("/get_user_transactions/{user_id:int}")
def get_user_transactions(user_id: int = fastapi.Path()):
    return crud.get_user_transactions(user_id)


if __name__ == "__main__":
    uvicorn.run("app:api", reload=True)
