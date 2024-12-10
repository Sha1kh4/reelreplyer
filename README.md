# Reel Replyer

## Overview

The Instagram Video Processor is a Python application that automates the downloading and processing of Instagram videos using the Symbl.ai API. It retrieves video content from Instagram Direct Messages, processes it for insights, and summarizes conversations based on the video content. This tool is designed for developers and marketers who want to leverage video content for enhanced engagement and analytics.

## Features

- **Download Videos**: Automatically downloads videos shared in Instagram Direct Messages.
- **Process Videos**: Sends downloaded videos to Symbl.ai for processing, extracting insights and conversation summaries.
- **Conversation Summaries**: Retrieves and displays conversation summaries based on processed video content.
- **Error Handling**: Implements robust error handling to manage API responses and token expiration.

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.x
- `pip` (Python package installer)
- Required Python packages:
  - `requests`
  - `python-dotenv`
  - `instagrapi`

You can install the required packages using:

```bash
pip install requests python-dotenv instagrapi
```

## Environment Variables

This project requires the following environment variables to be set in a `.env` file:

- `INSTAGRAM_USERNAME`: Your Instagram username.
- `INSTAGRAM_PASSWORD`: Your Instagram password.
- `SYMBL_APP_ID`: Your Symbl.ai application ID.
- `SYMBL_APP_SECRET`: Your Symbl.ai application secret.

Example of a `.env` file:

```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
SYMBL_APP_ID=your_symbl_app_id
SYMBL_APP_SECRET=your_symbl_app_secret
```

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Sha1kh4/reelreplyer
   cd reelreplyer
   ```

2. Install the required dependencies as mentioned above.

3. Create a `.env` file in the project root directory with your credentials.

4. Run the application:

   ```bash
   python main.py
   ```

5. The application will log in to your Instagram account, check for unread messages, download any video clips found, process them through the Symbl.ai API, and print out conversation summaries.

## Example Usage

![Example Usage](example.jpeg)

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- [Symbl.ai](https://symbl.ai) for providing the API used for processing video content.
- [Instagrapi](https://github.com/adw0rd/instagrapi) for enabling interaction with Instagram's private API.
