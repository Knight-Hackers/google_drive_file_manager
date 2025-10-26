### Google Drive File Manager

## Purpose and Goals

1. User is able to organize their files with the help of Google's AI model, Gemini. 
2. User will have to connect to their google drive to allow the application access to their files. 
3. A friendly map will be generated, showcasing AI suggestions on how to better organize the users drive.
4. Future implementation will include an interface that allows the user to make changes to their drive via the application. 

## Dependencies

1. Google Gemini API key
2. Google OAuth information (json file)
3. pip install googleapiclient, google 

## Obtaining Google Dependencies 

Generate a Gemini API key by navigating to Google AI Studio, clicking on "get API key" on the bottom right corner, and clicking on "create API key" on the top right corner. Create a new project in google cloud spaces. Under API's and Services, navigate to credentials. Make sure to create an API key, an OAuth 2.0 client ID, and a service account. Make sure to keep note of your provided API key and client ID. When creating your service account, download the json file associated with it. Keep the API key and client ID stored in a .env file within the same directory as the json file, which will be the Agents directory in this repository. 

# Bellow is an example of how your .env file should look like:

GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=YOUR_API_KEY
GOOGLE_CLOUD_PROJECT=YOUR_CLOUD_PROJECT
GOOGLE_CLOUD_LOCATION=LOCATION_PROVIDED
GOOGLE_SERVICE_ACCOUNT_JSON='path/to/.json'

GOOGLE_DRIVE_CLIENT_ID="client_id_in_OAuth.com"
GOOGLE_DRIVE_CLIENT_SECRET="YOUR_SECRET_KEY"
GOOGLE_DRIVE_REFRESH_TOKEN="YOUR_OBTAINED_REFRESH_TOKEN"
GOOGLE_DRIVE_SCOPES='https://www.googleapis.com/auth/drive.readonly' 

## Applications

Helps empower the user by providing suggestions towards a cleaner workspace. 

## How To Install

1. Make sure to download the requirements
2. Have node.js installed onto your computer
3. In front-end folder, you have to do an npm install
4. In back-end folder, you have to type in uvicorn main:app --host 127.0.0.1 --port 8000 --reload
