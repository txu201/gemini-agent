from google.adk.agents import Agent
from src.utils import create_horse_fact, roll_a_dice


root_agent = Agent(
    name="pro_search_agent",
    model="gemini-2.0-flash",
    instruction=(
        "You are a helpful research assistant that knows horse trivia. "
        "For any user prompt mentioning a horse, use create_horse_fact tool. "
        "For all other queries, use the roll_a_dice tool. "
    ),
    description="An agent that can answer questions.",
    tools=[create_horse_fact, roll_a_dice],
)
