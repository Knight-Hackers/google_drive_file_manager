from .BaseTool import BaseTool

class MindMap(BaseTool): 

    """
    Mind Map generator. 
    A tool for Gemini to give inputs to and it generates a mind map for the user to visualize their file usage.
    The bigger the files, the bigger the bubbles are.
    Goal is so that it can be organized by file type, category, size, and date. 
    """

    def __init__(self, task: str = "File type mind map"):

        super().__init__(
            name="Mind Map Generator", 
            description="An automated tool that outputs an image for users to visualize their file system", 
            supported_file_types=[".json"]
        )

        self.task = task

    def process_task(self, fileName: str = ".json") -> None: 

        """
        This tool will generate mind maps but in only certain categories.

        1. Based on file types (File type mind map)
        2. 
        """