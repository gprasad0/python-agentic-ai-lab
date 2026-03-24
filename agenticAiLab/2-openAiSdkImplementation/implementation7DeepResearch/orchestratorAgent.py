from pydantic import BaseModel
from dotenv import load_dotenv


class orchestratorAgent:

    def run(self, query: str):
        return "orchestrator"

    def sendNotification(self):
        return "send notification"

    def deepResearch(self):
        return "deep research"

    def plannerAgent(self):
        return "planner agent"
