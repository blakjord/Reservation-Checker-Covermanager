# CoverManager Reservation Checker

## Overview
CoverManager Reservation Checker is a Python script designed to automate the process of checking reservation availability at restaurants using the form created by CoverManager. The script periodically checks for new available reservation hours and notifies a Telegram group when new hours become available.

## Features

- Automatically checks reservation availability using the CoverManager form.
- Notifies a Telegram group when new reservation hours become available.
- Customizable configuration using a JSON file.
- Runs periodically to keep users updated with the latest reservation information.


## Example of Integrations
| Restaurant | Restaurant ID |
| -- | -- |
| Goiko El Bruc|goikogrill-bruc|
| Goiko Barcelona Diagonal |restaurante-CCDiagonalMarBarcelona|
| K-chopo|restaurante-kchopo|
| Umiko |umiko|
|Amazónico|restaurante-amazonico|
|Pai Pai|restaurante-paipai|

## Installation

For web access you will need to open port 777

## Option 1: Build and Run with Docker

Build the Docker image from the provided source code. Clone the repository and navigate to the root directory:
   ```bash
      docker build -t reservationchecker .
      docker run -p 777:777 reservationchecker
   ```

## Option 2: Execute with Python

If you wish to generate the Config/config.json file manually, you can do so based on the example file located at Config/Exampleconfig.json, as explained below.

Alternatively, you can generate the config.json file using the web portal. Execute the WEB/form_web.py Python script and access the web interface via port 777.

   ```bash
      python3 .\WEB\form_web.py
   ```
To run the bot when the Config/config.json file exist you need to execute the python:
   ```bash
      python3 .\main.py
   ```

## Deployment

### Initial Setup
When you run the Docker container for the first time or if the Config/config.json file does not exist, the web portal will be automatically activated. You have two ways to configure the bot.

#### Option 1 - Web Portal
If the Config/config.json file does not exist, you can access the web portal through port 777.

In the web portal, you can complete a form to configure the bot with the necessary data.
![Alt Text](https://i.ibb.co/L9sgfY5/imagen-2024-06-09-171344694.png)

#### Option 2 - Configuration File
You can edit the Config/config.json file directly to perform the configuration.

After editing the file, restart the Docker container to apply the changes.

## Configuration
Exist a example file config on Config/Exampleconfig.json.
The bot configuration includes the following parameters:


| Configuration | Configuration File | Description |
|-|-|-|
| Telegram Bot Token    | bot_token          | The bot token provided by BotFather.                                                             |
| Telegram Group ID     | group_id           | The ID of the group where messages will be sent.                                                 |
| Segundos Entre Escaneo| bucleCalls         | The time interval in seconds between each bot execution.                                          |
| URL Base                  | url                | The URL to which the bot will make calls to retrieve information.                                  |
| Dias a Restrear            | total_days         | The total number of days for which data will be fetched.                                           |
| Segundos Entre Llamada               | sleeper            | The waiting time in seconds between each API call.                                                 |
| Restaurant ID| restaurant_X       | The identifiers of the restaurants to which the bot will send requests.                            |

### Identifying the Restaurant ID
To identify the Restaurant ID, you can try the following methods:

#### Using the Web Portal:
Add the name of the restaurant in the appropriate field on the web portal and attempt to check it. The portal may provide the corresponding Restaurant ID upon successful verification.

#### Direct URL Access:

Try accessing the URL https://www.covermanager.com/reservation/module_restaurant/NOMBRERESTAURENTE, replacing NOMBRERESTAURENTE with the name of the restaurant. If the URL is accessible, it may reveal the Restaurant ID in the response or URL.

Using either method, you should be able to determine the Restaurant ID required for configuration.

#### Troubleshooting and Determining Restaurant ID
If you encounter difficulties determining the Restaurant ID, you can try the following methods:
1. Inspect Element:
Use the browser's developer tools to inspect the network requests sent by the web application.

Look for POST requests made when selecting a date or performing any action related to reservations.

Check the Referer header in the request headers or the URL parameters in the request. The Restaurant ID may be included at the end of the URL or in the request payload.
![Alt Text](https://i.ibb.co/HzQ7rcC/imagen-2024-06-09-193225086.png)
2. Create an Issue:

If you're facing challenges, you can create an issue in the repository. Describe the problem you're encountering, and someone from the community or the maintainers may assist you in resolving it.



## Authors

- [@blakjord](https://github.com/blakjord)

