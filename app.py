from dotenv import load_dotenv
from instagrapi import Client
import os
import requests
import tempfile
import time
import json
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

def download_video(video_url):
    """
    Downloads a video from the provided URL and saves it to a temporary file.
    """
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
        return temp_file.name


def get_access_token():
    """
    Retrieves the Symbl API access token .
    """
    url = "https://api.symbl.ai/oauth2/token:generate"

    payload = {
        "type": "application",
        "appId": "5a764f626d696741797361656f665636447566456252676c6542473267524652",
        "appSecret": "6e414b58685a61473368434c4a6c4742485a596a7a7a6568573539614f37344832715757706e62663479346d415541646c4c45387a5072687237766b69435249"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    responses = {
        400: 'Bad Request! Please refer docs for correct input fields.',
        401: 'Unauthorized. Please generate a new access token.',
        404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
        429: 'Maximum number of concurrent jobs reached. Please wait for some requests to complete.',
        500: 'Something went wrong! Please contact support@symbl.ai'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        # Successful API execution
        print("accessToken => " + response.json()['accessToken'])  # accessToken of the user
        print("expiresIn => " + str(response.json()['expiresIn']))  # Expiration time in accessToken
    elif response.status_code in responses.keys():
        print(responses[response.status_code], response.text)  # Expected error occurred
    else:
        print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))
    return response.json()['accessToken']

def process_video(temp_file_path, access_token):
    """
    Sends a video file to the Symbl API for processing.
    Automatically retries with a new access token if the current one is unauthorized.
    """
    url = "https://api.symbl.ai/v1/process/video"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "video/mp4"
    }

    try:
        with open(temp_file_path, "rb") as video_file:
            response = requests.post(url, headers=headers, data=video_file, params={"name": "Uploaded Video"})
            response.raise_for_status()
            return response.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Access token expired or unauthorized. Generating a new token...")
            new_access_token = get_access_token()
            headers["Authorization"] = f"Bearer {new_access_token}"
            with open(temp_file_path, "rb") as video_file:
                response = requests.post(url, headers=headers, data=video_file, params={"name": "Uploaded Video"})
                response.raise_for_status()
                print(response.json())
                return response.json()

        else:
            raise


def get_conversation_summary(conversation_id, access_token):
    """
    Retrieves the conversation summary from the Symbl API.
    """
    time.sleep(10)
    print(f'conversation id: {conversation_id}')
    url = f"https://api.symbl.ai/v1/conversations/{conversation_id}/summary"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Ensure 'summary' is a list before accessing it
    summary_data = response.json().get('summary', [])
    print(summary_data)
    return [item['text'] for item in summary_data if isinstance(item, dict)]

def process_instagram_video(video_url):
    """
    Downloads and processes an Instagram video using the Symbl API.
    """
    access_token = get_access_token()
    temp_file_path = download_video(video_url)
    try:
        # Process video and retrieve the conversation ID
        processing_response = process_video(temp_file_path, access_token)
        conversation_id = processing_response.get('conversationId')
        # Wait for processing to complete
        time.sleep(10)
        # Fetch and return conversation summary
        return get_conversation_summary(conversation_id, access_token)
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)


def main():
    # Initialize Instagram client
    cl = Client()
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    if not username or not password:
        raise ValueError("Instagram credentials not found in environment variables.")
    cl.login(username, password)

    while True:
        try:
            print("login ")
            # Fetch unread threads
            unread_threads = cl.direct_threads(amount=10, selected_filter="unread")
            for thread in unread_threads:
                print("received thread")
                # Fetch the most recent message in the thread
                recent_message = thread.messages[0] if thread.messages else None
                if recent_message.text:
                    print(f"Received message: {recent_message.text}")
                if recent_message and recent_message.clip and recent_message.clip.video_url:
                    video_url = recent_message.clip.video_url
                    
                    
                    print(f'video url: {video_url}')
                    summary = process_instagram_video(video_url)
                    print(f'summary: {summary}')
                    reply_message = "\n".join(summary)
                    print(f'reply message: {reply_message}')
                    # Reply to the thread
                    cl.direct_answer(thread_id=thread.id, text=reply_message)
            # Wait before the next check
            time.sleep(5)

        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()
