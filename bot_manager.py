import requests
import time

# Solana RPC URL (you can use a public RPC endpoint or set up your own local node)
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"

# The Solana account address you want to monitor
ACCOUNT_ADDRESS = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"  # Raydium Liquidity Pool V4

def get_confirmed_signatures_for_address(address, limit=10):
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [
            address,
            {"limit": limit}
        ]
    }
    response = requests.post(SOLANA_RPC_URL, headers=headers, json=payload)
    return response.json()

def get_transaction_details(signature):
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
    response = requests.post(SOLANA_RPC_URL, headers=headers, json=payload)
    return response.json()

def parse_transaction(transaction):
    # Extracting relevant information from the transaction
    transaction_info = {}
    if 'transaction' in transaction:
        transaction_info['signatures'] = transaction['transaction']['signatures']
        message = transaction['transaction']['message']
        transaction_info['instructions'] = message['instructions']
        if 'meta' in transaction:
            transaction_info['postBalances'] = transaction['meta'].get('postBalances', [])
            transaction_info['preBalances'] = transaction['meta'].get('preBalances', [])
            transaction_info['status'] = transaction['meta']['status']
    return transaction_info

def main():
    # Fetch confirmed signatures for the account
    signatures_response = get_confirmed_signatures_for_address(ACCOUNT_ADDRESS, limit=2)
    if 'result' in signatures_response:
        signatures = signatures_response['result']
        print(f"Found {len(signatures)} transactions for account {ACCOUNT_ADDRESS}")

        # Fetch transaction details for each signature
        pending_transactions = []
        for sig_info in signatures:
            signature = sig_info['signature']
            transaction_response = get_transaction_details(signature)
            if 'error' in transaction_response:
                if transaction_response['error']['code'] == 429:
                    print(f"Rate limit error for transaction {signature}. Waiting before retrying.")
                    time.sleep(10)  # Adjust this delay based on the API's rate limit policy
                else:
                    print(f"Failed to get details for transaction {signature}: {transaction_response['error']['message']}")
                continue

            if 'result' in transaction_response and transaction_response['result']:
                parsed_transaction = parse_transaction(transaction_response['result'])
                if parsed_transaction['status'] != 'Ok':
                    pending_transactions.append((signature, parsed_transaction))
            else:
                print(f"Failed to get details for transaction {signature}.")
            time.sleep(1)  # Add a delay to avoid rate limit errors

        # Print details of the last pending transaction
        if pending_transactions:
            print(f"Found {len(pending_transactions)} pending transactions.")
            for signature, details in pending_transactions:
                print(f"Transaction {signature} is pending.")
                pre_balances = details.get('preBalances', [])
                post_balances = details.get('postBalances', [])
                print(f"Transaction details: {details}")
                print(f"Pre-balances: {pre_balances}")
                print(f"Post-balances: {post_balances}")
        else:
            print("No pending transactions found.")
    else:
        print("Failed to fetch signatures for address")

if __name__ == "__main__":
    main()
