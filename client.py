import requests
import pydantic_models
from config import API_URL


def update_user(user: dict):
    user = pydantic_models.UserToUpdate.validate(user)
    response = requests.put(f'{API_URL}/user/{user.id}', data=user.json())
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return response.text


def delete_user(user_id: int):
    return requests.delete(f'{API_URL}/user/{user_id}').json()


def create_user(user: pydantic_models.UserToCreate):
    user = pydantic_models.UserToCreate.validate(user)
    return requests.post(f'{API_URL}/user/create', data=user.json()).json()


def get_info_about_user(user_id):
    return requests.get(f'{API_URL}/get_info_by_user_id/{user_id}').json()


def get_user_balance_by_id(user_id):
    response = requests.get(f'{API_URL}/get_user_balance_by_id/{user_id}')
    try:
        return float(response.text)
    except TypeError:
        return f'Error: Not a Number\nResponse: {response.text}'


def get_total_balance():
    response = requests.get(f'{API_URL}/get_total_balance')
    try:
        return float(response.text)
    except TypeError:
        return f'Error: Not a Number\nResponse: {response.text}'


def get_users():
    return requests.get(f"{API_URL}/users").json()


def get_user_wallet_by_tg_id(tg_id):
    user_dict = get_user_by_tg_id(tg_id)
    return requests.get(f"{API_URL}/get_user_wallet/{user_dict['id']}").json()


def get_user_by_tg_id(tg_id):
    return requests.get(f"{API_URL}/user_by_tg_id/{tg_id}").json()


def create_transaction(tg_id, receiver_address: str, amount_btc_without_fee: float):
    user_dict = get_user_by_tg_id(tg_id)
    payload = {'receiver_address': receiver_address,
               'amount_btc_without_fee': amount_btc_without_fee}
    response = requests.post(f"{API_URL}/create_transaction/{user_dict['id']}", json=payload)
    return response.text
