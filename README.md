# sol_sandwich_bot

## Requirements

- Python 3.5

## Setup
To set up the app locally, follow these steps:

1. Clone the repository to your local machine:
    ```sh
    git clone https://github.com/your-username/sol_sandwich_bot.git
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    ```sh
    source venv/bin/activate
    ```

4. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### File structure

README.md            # Project description and instructions for setup and usage

config.py            # Configuration file containing project settings

requirements.txt     # List of dependencies required for the project

tests/               # Directory for unit and integration tests

### Configuration

1. Create a `.env` file by copying the example file:
    ```sh
    cp .env.example .env
    ```

2. Update the `.env` file with your desired configuration:
    ```env
      SOLANA_RPC_URL='https://api.mainnet-beta.solana.com'
    ```

### Running the App

To run the application, execute:
```sh
python3 bot_manager.py
```

### Running Tests

To run the unit tests, execute:
```sh
python -m unittest discover -s tests
```

### Author
Sergey Chernyakov
```








sol_sandwich_bot % python3 bot_manager.py
Found 2 transactions for account 675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8
Rate limit error for transaction 5sVVigtXfmEMU6VPZvxh7qdD9Jff26mf6P8AtX2XZCJeaDAQdRpbuJpUQrj5aPAYY3N78RYixWzNvhTVZBQvbLXG. Waiting before retrying.
Found 1 pending transactions.
Transaction 5wjqAoeoak9VhMjpwYjtbzLaLKn98GLEiVd5cNMLBDSvTHqAJn2k2vo1kUDJigDinApfGa3qnVvE1XWkfwDg42Ja is pending.
Transaction details: {'signatures': ['5wjqAoeoak9VhMjpwYjtbzLaLKn98GLEiVd5cNMLBDSvTHqAJn2k2vo1kUDJigDinApfGa3qnVvE1XWkfwDg42Ja'], 'instructions': [{'accounts': [], 'data': 'HMypLP', 'programIdIndex': 6, 'stackHeight': None}, {'accounts': [], 'data': '3u6scRsPBrLX', 'programIdIndex': 6, 'stackHeight': None}, {'accounts': [0, 3, 0, 7, 41, 35], 'data': '2', 'programIdIndex': 8, 'stackHeight': None}, {'accounts': [0, 35, 33, 32, 3, 37, 27, 28, 26, 29, 5, 30, 31, 40, 37, 21, 16, 22, 4, 1, 20, 15, 34, 39, 17, 38, 19, 2, 11, 23, 36, 13, 25, 18, 24, 14, 12, 10], 'data': 's99vUtFMRbjCiAN3prqRNud', 'programIdIndex': 9, 'stackHeight': None}], 'postBalances': [27079523695, 70407360, 16258560, 0, 70407360, 70407360, 1, 51461600, 731913600, 1141440, 0, 2039280, 2039280, 3591360, 2039280, 70407360, 2039280, 6124800, 113448000, 23357760, 70407360, 5435760, 2039280, 83779311134, 79928640, 113448000, 2039280, 946585870, 71626990165444, 70407360, 70407360, 70407360, 2039280, 798006064463, 0, 934087680, 1141440, 1141440, 3865064002, 1141440, 0, 1], 'preBalances': [27079529097, 70407360, 16258560, 0, 70407360, 70407360, 1, 51461600, 731913600, 1141440, 0, 2039280, 2039280, 3591360, 2039280, 70407360, 2039280, 6124800, 113448000, 23357760, 70407360, 5435760, 2039280, 83779311134, 79928640, 113448000, 2039280, 946585870, 71626990165444, 70407360, 70407360, 70407360, 2039280, 798006064463, 0, 934087680, 1141440, 1141440, 3865064002, 1141440, 0, 1], 'status': {'Err': {'InstructionError': [3, {'Custom': 6002}]}}}
Pre-balances: [27079529097, 70407360, 16258560, 0, 70407360, 70407360, 1, 51461600, 731913600, 1141440, 0, 2039280, 2039280, 3591360, 2039280, 70407360, 2039280, 6124800, 113448000, 23357760, 70407360, 5435760, 2039280, 83779311134, 79928640, 113448000, 2039280, 946585870, 71626990165444, 70407360, 70407360, 70407360, 2039280, 798006064463, 0, 934087680, 1141440, 1141440, 3865064002, 1141440, 0, 1]
Post-balances: [27079523695, 70407360, 16258560, 0, 70407360, 70407360, 1, 51461600, 731913600, 1141440, 0, 2039280, 2039280, 3591360, 2039280, 70407360, 2039280, 6124800, 113448000, 23357760, 70407360, 5435760, 2039280, 83779311134, 79928640, 113448000, 2039280, 946585870, 71626990165444, 70407360, 70407360, 70407360, 2039280, 798006064463, 0, 934087680, 1141440, 1141440, 3865064002, 1141440, 0, 1]
