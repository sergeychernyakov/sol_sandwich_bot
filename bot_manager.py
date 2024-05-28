import requests
import time
from config import Config

class BotManager:
    def __init__(self):
        config = Config()
        self.account_address = config.ACCOUNT_ADDRESS
        self.rpc_url = config.SOLANA_RPC_URL

    def get_confirmed_signatures_for_address(self, limit=10):
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                self.account_address,
                {"limit": limit}
            ]
        }
        response = requests.post(self.rpc_url, headers=headers, json=payload)
        return response.json()

    def get_transaction_details(self, signature):
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
        return response.json()

    def parse_transaction(self, transaction):
        # Extracting relevant information from the transaction
        transaction_info = {}
        if 'transaction' in transaction:
            transaction_info['signatures'] = transaction['transaction']['signatures']
            message = transaction['transaction']['message']
            transaction_info['instructions'] = message['instructions']
            if 'meta' in transaction:
                transaction_info['postBalances'] = transaction['meta'].get('postBalances', [])
                transaction_info['preBalances'] = transaction['meta'].get('preBalances', [])
                transaction_info['status'] = transaction['meta'].get('status', {})
        return transaction_info

    def is_transaction_pending(self, transaction_response):
        # Check if the transaction is pending
        if 'result' not in transaction_response or transaction_response['result'] is None:
            return True
        return False

    def run(self):
        while True:
            # Fetch confirmed signatures for the account
            signatures_response = self.get_confirmed_signatures_for_address(limit=2)
            if 'result' in signatures_response:
                signatures = signatures_response['result']
                print(f"Found {len(signatures)} transactions for account {self.account_address}")

                # Fetch transaction details for each signature
                pending_transactions = []
                for sig_info in signatures:
                    signature = sig_info['signature']
                    transaction_response = self.get_transaction_details(signature)
                    if 'error' in transaction_response:
                        if transaction_response['error']['code'] == 429:
                            print(f"Rate limit error for transaction {signature}. Waiting before retrying.")
                            time.sleep(1)  # Adjust this delay based on the API's rate limit policy
                            break
                        else:
                            print(f"Failed to get details for transaction {signature}: {transaction_response['error']['message']}")
                        continue

                    if self.is_transaction_pending(transaction_response):
                        print(f"Transaction {signature} is pending.")
                        pending_transactions.append((signature, self.parse_transaction(transaction_response.get('result', {}))))
                    time.sleep(1)  # Add a delay to avoid rate limit errors

                # Print details of the pending transactions
                if pending_transactions:
                    print(f"Found {len(pending_transactions)} pending transactions.")
                    for signature, details in pending_transactions:
                        print(f"Transaction {signature} is pending.")
                        pre_balances = details.get('preBalances', [])
                        post_balances = details.get('postBalances', [])
                        print(f"Transaction details: {details}")
                        print(f"Pre-balances: {pre_balances}")
                        print(f"Post-balances: {post_balances}")
                        print(f"Instructions: {details['instructions']}")
                        print(f"Status: {details['status']}")
                else:
                    print("No pending transactions found.")
            else:
                print("Failed to fetch signatures for address")

            # Wait a bit before checking for new transactions
            time.sleep(20)

if __name__ == "__main__":
    bot_manager = BotManager()
    bot_manager.run()
