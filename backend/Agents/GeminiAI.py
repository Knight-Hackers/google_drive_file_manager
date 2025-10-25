from dotenv import load_dotenv
from .BaseAgent import BaseAgent
import os
from typing import List, Dict, Any, Optional
from google import genai

load_dotenv()

class GeminiAI(BaseAgent):

    """
    AI agent that uses all the tools within the folder to answer user queries
    Uses FileManager to gain access to files, organize them and output via json, and sends it back to FileManager so that it can process the request. 
    """

    def __init__(self, tools: Dict[str, object] = None, model: str = "gemini-2.5-flash"):

        super().__init__(
            name="Gemini AI Agent", 
            role=
            """
            You are an AI agent that utilizes various tools to help users with their file management requests. You will provide insightful and accurate responses that will help the users organize their google cloud. 
            
            Your responses will be in the form of a json file that contains the following: 

            1. Message: Your full response.
            2. Tools: Any tools that you think are necessary to complete the task. Should be in the format of a dictionary/json file that contains the tool as the header and what it's going to do as the content.
            3. Suggestions: Anything the user can do to avoid file clutter based on what you saw.

            Some of the many tasks you can do are: 

            1. Generate a json file that provides feeback on what would be best to organize the users files. 
            2. Provide inputs within the json file so that another tool can generate a mind map off of it.
            3. Send requests to a tool so that it can process your request and act on it to organize the users drive.
            
            """
        )

        GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

        self.model = model
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def process_message(self, message: str):

        """
        Method that processes the users message and outputs the response of the AI model

        Args: 
            User Message

        Output: 
            AI response
        """

        input_message = self.role + "\n\nPlease respond the the following message accordingly.\n\n" + message

        response = self.client.models.generate_content(
            model="gemini-2.5-flash", contents=input_message
        )

        return response.text