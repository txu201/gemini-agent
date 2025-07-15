from dotenv import load_dotenv
load_dotenv()

from .orchestrator import SmartOrchestrator

root_agent = SmartOrchestrator()
__all__ = ["root_agent"]
