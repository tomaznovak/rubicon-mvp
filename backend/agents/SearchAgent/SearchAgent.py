from agency_swarm.agents import Agent
from backend.agents.SearchAgent.tools import arxiv_tool, script_tool, find_path_tool, search_tool


class SearchAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            name="Timi",
            description="You are a professional gatherer of the information.",
            instructions="./instructions.md",
            files_folder="",
            tools=[arxiv_tool.arxiv_tool, script_tool.script_tool, find_path_tool.find_path_tool, search_tool.search_tool],
            tools_folder="./tools",
            temperature=0,
            max_prompt_tokens=25000,
            model="gpt-4o",
            **kwargs
        )


        