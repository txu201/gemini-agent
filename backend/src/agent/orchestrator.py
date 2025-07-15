from google.adk.orchestrators import AgentOrchestrator
from .agent_search import agent_search
from .agent import root_agent

class SmartOrchestrator(AgentOrchestrator):
    def route(self, task: str):
        # Route to custom tool agent if task contains 'horse' or 'dice'
        if "horse" in task.lower() or "dice" in task.lower():
            return root_agent
        else:
            return agent_search
