# Gmail Zapper

Gmail Zapper is a Python application that utilizes the Gmail API to fetch and display emails from specific sender addresses with optional search criteria. It provides a graphical user interface (GUI) to view email bodies and navigate through the fetched emails.

## Features

- Fetches emails from specific sender addresses with optional search criteria
- Displays email bodies in a GUI for easy viewing
- Allows navigation between fetched emails

## In development
- Automatic printing PDF files from specific sender addresses with optional search criteria (useful for utility bills)

## Prerequisites

Before running the application, make sure you have completed the following steps:

1. Install Python (version 3.11.X or later)
2. Install the required packages by running the following command:

> pip install -r requirements.txt

3. Set up Google API credentials by following the instructions in the "Setup Google API Credentials" section below.

## Setup Google API Credentials

To use the Gmail API, you need to set up Google API credentials. Follow these steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Gmail API for your project.
4. Create OAuth 2.0 credentials.
5. Download the credentials file (JSON format) and save it as `credentials.json` in the project directory.

## Usage

To run the Email Viewer application, execute the following command:

> python main.py

If you are using a Linux OS
> python3 main.py

The application will launch the GUI, where you can specify the sender addresses and search criteria. Click the "Next" button to navigate through the fetched emails and view their bodies.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the application, feel free to submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
