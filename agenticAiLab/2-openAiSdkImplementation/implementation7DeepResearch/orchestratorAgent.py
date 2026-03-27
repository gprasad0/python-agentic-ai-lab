from pydantic import BaseModel
from dotenv import load_dotenv


class OrchestratorAgent:

    def run(self, query: str):
        yield "Planning searches..."

    def sendNotification(self):
        return "send notification"

    def deepResearch(self):
        return "deep research"

    def plannerAgent(self):
        return "planner agent"
