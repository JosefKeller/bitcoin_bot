import fastapi
import uvicorn
import database
import pydantic_models
import config
import copy

api = fastapi.FastAPI()

fake_database = {'users': [
    {
        "id":1,
        "name":"Anna",
        "nick":"Anny42",
        "balance": 15300
     },

    {
        "id":2,
        "name":"Dima",
        "nick":"dimon2319",
        "balance": 160.23
     }
    ,{
        "id":3,
        "name":"Vladimir",
        "nick":"Vova777",
        "balance": 200.1
     }
],
}


@api.delete('/user/{user_id}')
def delete_user(user_id: int = fastapi.Path()):
    for index, u in enumerate(fake_database['users']):
        if u['id'] == user_id:
            old_db = copy.deepcopy(fake_database)
            del fake_database['users'][index]    # удаляем юзера из бд
            return {'old_db': old_db,
                    'new_db': fake_database}


@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.User = fastapi.Body()):
    for index, u in enumerate(fake_database['users']):
        if u['id'] == user_id:
            fake_database['users'][index] = user.dict()
            return user


@api.post('/user/create')
def index(user: pydantic_models.User):
    fake_database['users'].append(user.dict())
    return {'User Created!': user}


@api.get('/users')
def get_users(skip: int = 0, limit: int = 10):
    return fake_database['users'][skip:skip+limit]


@api.get('/get_info_by_user_id/{id:int}')
def get_info_about_user(id):
    return fake_database['users'][id-1]


@api.get('/get_user_balance_by_id/{id:int}')
def get_user_balance(id):
    return fake_database['users'][id-1]['balance']


@api.get('/get_total_balance')
def get_total_balance():
    total_balance: float = 0.0
    for user in fake_database['users']:
        total_balance += pydantic_models.User(**user).balance
    return total_balance


if __name__ == "__main__":
    uvicorn.run("app:api", reload=True)
