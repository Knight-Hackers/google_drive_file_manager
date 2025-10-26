from typing import List, Dict, Any, Optional
import google.generativeai as genai
from datetime import datetime
import json
import asyncio
from pathlib import Path
import os
from BaseTool import BaseTool

class BaseAgent:
    """Base class for all agents with core message processing and tool handling capabilities."""

    def __init__(self, 
                 name: str, 
                 role: str,
                 tools: Dict[str, object] = None):
        """
        Initialize the base agent.
        
        Args:
            name (str): Name of the agent
            description (str): Description of the agent's purpose
            tools (Dict[str, object]): Any necessary tools for the Agent
        """
        self.name = name
        self.role = role
        
        # Initialize tools 
        self.tools: Dict[str, object] = {} if tools is None else tools
    
    def add_tool(self, tool: BaseTool) -> None: 

        """
        Add a tool to the agent's toolkit.
        
        Args:
            tool (object): The tool object to add
        """

        if tool.name not in self.tools: 
            self.tools[tool.name] = tool
