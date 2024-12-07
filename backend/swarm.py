from agency_swarm import Agency, set_openai_key
from backend.agents.SearchAgent import SearchAgent
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
set_openai_key(openai_api_key)

searcher = SearchAgent()

agency = Agency([
    searcher
    ], max_completion_tokens=25000
)
# agency.run_demo()
