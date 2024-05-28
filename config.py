import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')
    SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL')
