import requests
import time
import asyncio
from asyncstdlib import enumerate
from solana.rpc.websocket_api import connect
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solders.rpc.config import RpcTransactionLogsFilterMentions
from config import Config
import webbrowser
import base58

class BotManager:
    def __init__(self, rpc_service='solana', commitment='finalized'):
        # "confirmed", "finalized" or "processed"
        config = Config()
        self.account_address = config.ACCOUNT_ADDRESS
        if rpc_service == 'quicknode':
            self.rpc_url = config.QUICKNODE_RPC_URL
            self.ws_url = config.QUICKNODE_WS_URL
        else:
            self.rpc_url = config.SOLANA_RPC_URL
            self.ws_url = config.SOLANA_WS_URL
        self.commitment = commitment 

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
                    "commitment": self.commitment,
                    "limit": limit
                }
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
        # print(response.json())
        if 'result' not in response.json() or response.json()['result'] is None:
            return None
        return response.json()

    def parse_transaction(self, transaction):
        # Extract relevant information from the transaction
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

    def open_transaction_in_browser(self, signature):
        url = f"https://solscan.io/tx/{signature}"
        webbrowser.open(url)

    async def logs_subscribe(self) -> None:
        """Subscribe to logs for the Solana account and listen for pending transactions."""
        async with connect(self.ws_url) as websocket:
            pubkey = Pubkey(base58.b58decode(self.account_address))
            filter_ = RpcTransactionLogsFilterMentions(pubkey)
            await websocket.logs_subscribe(filter_, commitment=self.commitment)
            first_resp = await websocket.recv()
            subscription_id = first_resp[0].result
            print(f"Subscribed to logs for account {self.account_address} with subscription ID {subscription_id}")
            async for idx, msg in enumerate(websocket):
                self.process_log_notification(msg)

    def process_log_notification(self, msg):
        """Process incoming log notifications."""

        # Check if the message is a list and get the first element
        if isinstance(msg, list) and len(msg) > 0:
            notification = msg[0]
        else:
            notification = msg

        # Check if the notification has a result attribute
        if hasattr(notification, 'result'):
            result = notification.result

            # Accessing the context and value
            context = result.context
            value = result.value

            if value.err is not None:
                # print(f"Error: {value.err}")
                return

            # Printing out the slot number
            print(f"Slot: {context.slot}")

            # Printing the signature
            print(f"<<<--- Signature: https://solscan.io/tx/{value.signature}")
            
            # self.open_transaction_in_browser(value.signature)

            # Printing the logs
            print("Logs:")
            for log in value.logs:
                print(log)
                # if "Instruction: Transfer" in log:
                #     print(f"Token Transfer Detected: {log}")

    def run(self):
        while True:
            # Get confirmed signatures for the account
            signatures_response = self.get_confirmed_signatures_for_address(limit=10)
            if 'result' in signatures_response:
                signatures = signatures_response['result']
                print(f"Found {len(signatures)} transactions for account https://solscan.io/tx/{self.account_address}")

                # Filter out transactions without errors and with 'processed' status
                filtered_signatures = [sig['signature'] for sig in signatures if sig['err'] is None]

                pending_transactions = []
                for signature in filtered_signatures:
                    # self.open_transaction_in_browser(signature) # Open page in the browser
                    transaction_response = self.get_transaction_details(signature)
                    if transaction_response is None:
                        print(f"Transaction details for https://solscan.io/tx/{signature} are not available.")
                        continue
                    if 'result' in transaction_response:
                        print(f"Transaction {signature} is pending.")
                        parsed_transaction = self.parse_transaction(transaction_response['result'])
                        pending_transactions.append((signature, parsed_transaction))
                    time.sleep(1)  # Add a delay to avoid rate limit errors

                # Print details of pending transactions
                if pending_transactions:
                    print(f"Found {len(pending_transactions)} pending transactions.")
                    for signature, details in pending_transactions:
                        print(f"Transaction {signature} is pending.")
                        pre_balances = details.get('preBalances', [])
                        post_balances = details.get('postBalances', [])
                        instructions = details.get('instructions', [])
                        status = details.get('status', {})
                        print(f"Transaction details: {details}")
                        print(f"Pre-balances: {pre_balances}")
                        print(f"Post-balances: {post_balances}")
                        print(f"Instructions: {instructions}")
                        print(f"Status: {status}")
                else:
                    print("No pending transactions found.")
            else:
                print("Failed to fetch signatures for address")

            # Wait before checking for new transactions
            time.sleep(20)

if __name__ == "__main__":
    bot_manager = BotManager(rpc_service='quicknode', commitment='processed') # "confirmed", "finalized" or "processed"
    # bot_manager.run()

    asyncio.run(bot_manager.logs_subscribe())
