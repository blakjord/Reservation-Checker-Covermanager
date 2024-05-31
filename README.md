# CoverManager Reservation Checker

## Overview

CoverManager Reservation Checker is a Python script designed to automate the process of checking reservation availability at restaurants using the form created by CoverManager. The script periodically checks for new available reservation hours and notifies a Telegram group when new hours become available.

## Features

- Automatically checks reservation availability using the CoverManager form.
- Notifies a Telegram group when new reservation hours become available.
- Customizable configuration using a JSON file.
- Runs periodically to keep users updated with the latest reservation information.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/CoverManager-Reservation-Checker.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the script by editing the `config.json` file with your settings.

4. Run the script:

   ```bash
   python covermanager_reservation_checker.py
   ```

## Configuration

You can configure the script by editing the `config.json` file. Here are the available configuration options:

- `url`: The URL of the CoverManager form.
- `restaurant`: The ID of the restaurant.
- `total_days`: Number of days to search for reservation availability.
- `sleeper`: Time interval (in seconds) between each check.
- `bot_token`: The Telegram bot token.
- `group_id`: The ID of the Telegram group.
- `bucleCalls`: Interval (in seconds) between each execution of the script.

## Usage

Simply run the script, and it will periodically check for new reservation hours. You will receive notifications in your Telegram group when new hours become available.

## Contributing

Contributions are welcome! If you have any ideas for improvements or find any issues, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
