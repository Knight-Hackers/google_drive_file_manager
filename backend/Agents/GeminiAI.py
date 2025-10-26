from dotenv import load_dotenv
from BaseAgent import BaseAgent
import os
from typing import List, Dict, Any, Optional, Union
from google import genai
import json
import re
import ast
from FileManager import FileManager
from MindMap import MindMap # Boilerplate for now, will have to look into other implementations

load_dotenv()

class GeminiAI(BaseAgent):

    """
    AI agent that uses all the tools within the folder to answer user queries
    Uses FileManager to gain access to files, organize them and output via json, and sends it back to FileManager so that it can process the request. 
    """

    def __init__(self, model: str = "gemini-2.5-flash"):

        super().__init__(
            name="Gemini AI Agent", 
            role=
            """
            You are an AI agent that utilizes various tools to help users with their file management requests. You will provide insightful and accurate responses that will help the users organize their google drive. 
            
            Your responses will be in the form of a json file that contains the following: 

            1. Message: Your full response.
            2. Tools: An array of any tools that you think are necessary to complete the task. Should be in the format of a dictionary with the header as the tool name and the content is what its going to be used for.
            3. CategorizedFileList: A list that contains an array of size 2 where at index 0 exists the category and at index 1 the filename.

            Your initial response should look as such: 

            {
                "Message": your response, 
                "Tools": an array of tools you think is best for the job, 
                "CategorizedFileList": An n x 2 matrix that containts the file names alongside the category you think suits them best
            }

            Some of the many tasks you can do are: 

            1. Generate a json file that provides feeback on what would be best to organize the users files. 
            2. Provide inputs within the json file so that another tool can generate a mind map off of it.
            3. Send requests to a tool so that it can process your request and act on it to organize the users drive.

            The tools available to you are: 

            1. FileManager: A tool that can provide access to the files within the users google drive. 
            2. MindMap: A tool that you output json files to so that it can create mind maps based on that. 
            """
        )

        GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

        self.model = model
        self.client = genai.Client(api_key=GEMINI_API_KEY)

        self.tools: Dict[str, (FileManager, MindMap)] = {
            "FileManager": FileManager(),
            "MindMap": MindMap()
        }

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

        # strip surrounding fences or whitespace
        output = response.text.strip()
        # remove leading/trailing triple-backticks and optional language token
        output = re.sub(r'^\s*```(?:json|txt)?\s*', '', output, flags=re.I)
        output = re.sub(r'\s*```\s*$', '', output)

        # Try JSON first
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            pass

        # Try Python literal evaluation (handles single quotes, trailing commas sometimes)
        try:
            return ast.literal_eval(output)
        except Exception:
            pass

        return output
    
        # if "FileManager" in output["Tools"]:
        #     self.process_file_request(output["Tools"]["FileManager"])
        
        # if "MindMap" in output["Tools"]:
        #     self.process_mind_map_request(output["Tools"]["MindMap"])

        
    def process_file_request(self, task):

        self.tools["FileManager"].run(task)

    def process_mind_map_request(self, task):

        self.tools["MindMap"].run(task)