import requests
import time
from config import Config

class BotManager:
    def __init__(self):
        config = Config()
        self.account_address = config.ACCOUNT_ADDRESS
        self.rpc_url = config.SOLANA_RPC_URL

    def get_confirmed_signatures_for_address(self, limit=1000):
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                self.account_address,
                {
                    "commitment": "confirmed", # "confirmed", # можно использовать также "finalized" или "processed"
                    "limit": limit
                }
            ]
        }
        response = requests.post(self.rpc_url, headers=headers, json=payload)
        return response.json()

    def get_transaction_details(self, signature):
        # commitment "processed" is not supported.
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [
                signature,
                {"encoding": "json", "maxSupportedTransactionVersion": 0}
            ]
        }
        response = requests.post(self.rpc_url, headers=headers, json=payload)
        print(response.json())
        if 'result' not in response.json() or response.json()['result'] is None:
            return None
        return response.json()

    def parse_transaction(self, transaction):
        # Извлечение релевантной информации из транзакции
        transaction_info = {}
        if transaction is None:
            return transaction_info
        if 'transaction' in transaction:
            transaction_info['signatures'] = transaction['transaction'].get('signatures', [])
            message = transaction['transaction'].get('message', {})
            transaction_info['instructions'] = message.get('instructions', [])
            if 'meta' in transaction:
                transaction_info['postBalances'] = transaction['meta'].get('postBalances', [])
                transaction_info['preBalances'] = transaction['meta'].get('preBalances', [])
                transaction_info['status'] = transaction['meta'].get('status', {})
        return transaction_info

    def run(self):
        while True:
            # Получение подтвержденных подписей для аккаунта
            signatures_response = self.get_confirmed_signatures_for_address(limit=10)
            if 'result' in signatures_response:
                signatures = signatures_response['result']
                print(f"Найдено {len(signatures)} транзакций для аккаунта {self.account_address}")

                print('!!!!!!! Подписи:')
                print(signatures)

                # Фильтрация транзакций без ошибок и со статусом 'processed'
                filtered_signatures = [sig['signature'] for sig in signatures if sig['err'] is None]

                print('!!!!!!! Отфильтрованные подписи:')
                print(filtered_signatures)

                pending_transactions = []
                for signature in filtered_signatures:
                    transaction_response = self.get_transaction_details(signature)
                    if transaction_response is None:
                        print(f"Детали транзакции для {signature} не доступны.")
                        continue
                    if 'result' in transaction_response:
                        print(f"Transaction {signature} is pending.")
                        parsed_transaction = self.parse_transaction(transaction_response['result'])
                        pending_transactions.append((signature, parsed_transaction))
                    time.sleep(1)  # Добавление задержки для избежания ошибок лимита скорости

                # Печать деталей неподтвержденных транзакций
                if pending_transactions:
                    print(f"Найдено {len(pending_transactions)} неподтвержденных транзакций.")
                    for signature, details in pending_transactions:
                        print(f"Транзакция {signature} находится в ожидании.")
                        pre_balances = details.get('preBalances', [])
                        post_balances = details.get('postBalances', [])
                        instructions = details.get('instructions', [])
                        status = details.get('status', {})
                        print(f"Детали транзакции: {details}")
                        print(f"Балансы до: {pre_balances}")
                        print(f"Балансы после: {post_balances}")
                        print(f"Инструкции: {instructions}")
                        print(f"Статус: {status}")
                else:
                    print("Не найдено неподтвержденных транзакций.")
            else:
                print("Не удалось получить подписи для адреса")

            # Ожидание перед проверкой новых транзакций
            time.sleep(20)

if __name__ == "__main__":
    bot_manager = BotManager()
    bot_manager.run()
