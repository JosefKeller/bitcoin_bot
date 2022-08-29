import datetime
import config
import pydantic_models
import models
import bit

wallet = bit.PrivateKeyTestnet(config.TESTNET_WALLET)
print(f"Баланс: {wallet.get_balance()}")
print(f"Адрес: {wallet.address}")
print(f"Приватный ключ: {wallet.to_wif()}")
print(f"Все транзакции: {wallet.get_transactions()}")

# transaction = wallet.send([('muh9DYMTWXfPEd9zPnfvCS1yX8hPLbkE9e', 1, 'rub')])
# print(transaction)
