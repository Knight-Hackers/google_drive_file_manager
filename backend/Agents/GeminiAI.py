from dotenv import load_dotenv
from BaseAgent import BaseAgent
import os
from typing import List, Dict, Any, Optional, Union
from google import genai
from google.genai import types
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

            1. Message: Your full response to the users initial query.
            2. Tools: A dictionary of any tools that you think are necessary to complete the task. Should be in the format of a dictionary with the header as the tool name and the content is what its going to be used for.
            3. CategorizedFileList: A list that contains a matrix of size n x 2 where at column 0 exists the category of a file and at column 1 the filename.

            If you plan on using FileManager, make sure the content is as follows: 

            1. the function call 'list_files' that accepts a query and page size and returns a list of the files in the drive
            2. the function call 'count_files' that accepts a query and returns the amount of files in the drive
            3. the function call 'get_file' that accepts a file_id returns the metadata of a specific file
            4. the function call 'list_folder' that accepts a folder_id and returns a list of folders
            5. the function call 'retrieve_file' that accepts a file_id and an export_mime and outputs the contents of a file
            
            Ex: A payload input for the 'list_files' function would be:
                payload={
                    'action': 'list_files', 
                    'q': 'trashed = false', 
                    'page_size': 100
                }

            If you plan on using MindMap, make sure the content is as follows: 
                1. a json file that contains 'data' header with the contents of what would be best for the MindMap

            Ex: A payload input for the 'execute' function would be: 
                payload={
                    'data': {'files': []}, 
                    'output_path': 'mindmap.png'
                }

            Or: 
                payload={
                    'json_path': '.json',
                    'map_type': 'file_size'
                }

            Your initial response to any user input should look as such: 

            {
                "Message": your response to the initial prompt, 
                "Tools": a dictionary of tools you think is best for the job, 
                "CategorizedFileList": An n x 2 matrix that containts the file names alongside the category you think suits them best
            }

            Some of the many tasks you can do are: 

            1. Generate a json file that provides feeback on what would be best to organize the users files. 
            2. Provide inputs within the json file so that another tool can generate a mind map off of it.
            3. Send requests to a tool so that it can process your request and act on it to organize the users drive.

            The json file output for the MindMap will have three headers ("total_files", "categories", "files"). Within the "total_files" category will be an integer that states the number of files present in the drive. The "categories" header will contain a dictionary with categories that you generated based on the files you looked at and how many are in each category. The "files" header will contain a list of dictionaraires that each have two headers (one for the file name and another for the category that the file belongs to). 
            
            An example of an output for the MindMap json file structure is as follows: 

            {
                "Tools": "MindMap",
                "total_files": 3,
                "categories": {
                    "school": 1,
                    "work": 1,
                    "personal": 1
                },
                "files": [
                    {"name": "Math_Homework.docx", "category": "school"},
                    {"name": "Team_Project_Report.docx", "category": "work"},
                    {"name": "My_Resume.docx", "category": "personal"}
                ]
            }

            The tools available to you are: 

            1. FileManager: A tool that can provide access to the files within the users google drive. 
            2. MindMap: A tool that you output json files to so that it can create mind maps based on that. 
            """
        )

        GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

        self.model = model
        self.client = genai.Client(api_key=GEMINI_API_KEY)

        # Geminis tool access
        self.fm = FileManager()
        self.mm = MindMap()

        # Grab File Names
        files = self.fm.list_files()
        file_names = [file['name'] for file in files]

        out = self.process_message(message="", file_names=file_names)
        print(out)

    def process_message(self, message: str = "", file_names: List[Dict[str, Any]] = []):

        """
        Method that processes the users message and outputs the response of the AI model

        Args: 
            User Message

        Output: 
            AI response
        """

        input_message = [message + "\n\n" + self.role]
        for i in range(len(file_names) - 1):
            input_message.append(file_names[i])

        response = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=input_message
        )

        # strip surrounding fences or whitespace
        output = response.text.strip()
        # remove leading/trailing triple-backticks and optional language token
        output = re.sub(r'^\s*```(?:json|txt)?\s*', '', output, flags=re.I)
        output = re.sub(r'\s*```\s*$', '', output)

        # Try JSON first
        try:
            output = json.loads(output)
        except json.JSONDecodeError:
            pass

        # Try Python literal evaluation (handles single quotes, trailing commas sometimes)
        try:
            output = ast.literal_eval(output)
        except Exception:
            pass
    
        return output
        
    def process_file_request(self, task={'action': 'list_files', 'q': 'trashed = false', 'page_size': 100}):
        """
        Post-message processing, FileManager tool acts to collect files from the drive
        """
        self.fm.run(task)

    def process_mind_map_request(self, task={'data': {'files': []}, 'output_path': 'mindmap.png'}): # Boilerplate
        """
        Post-message processing, MindMap Generator tool acts to generate maps for the user
        """
        self.mm.run(task)