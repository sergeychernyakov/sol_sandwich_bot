# Solana Sandwich Bot

## Requirements

- Python 3.5+

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

