import pytest
import asyncio
from types import SimpleNamespace
from google.adk.tools import google_search
from src.utils import create_horse_fact, roll_a_dice
from src.agent_search import agent_search
from src.agent import root_agent as custom_agent
from src.orchestrator import SmartOrchestrator

async def _collect(gen):
    items = []
    async for item in gen:
        items.append(item)
    return items

# Helper to collect results from async generator in sync tests
def collect(gen):
    return asyncio.get_event_loop().run_until_complete(_collect(gen))


def test_create_horse_fact_returns_valid():
    facts = [
        "Horses cannot sleep.",
        "Horses have a unique way of communicating with each other through body language.",
        "The fastest recorded speed of a horse is 55 mph (88.5 km/h)."
    ]
    fact = create_horse_fact()
    assert fact in facts


def test_roll_a_dice_range():
    for _ in range(10):
        val = roll_a_dice()
        assert 1 <= val <= 6


def test_agent_search_has_google_search():
    assert google_search in agent_search.tools


def test_custom_agent_has_tools():
    tools = custom_agent.tools
    assert create_horse_fact in tools
    assert roll_a_dice in tools

class DummyEvent:
    def __init__(self, content):
        self.content = content

class DummyCtx:
    def __init__(self, text):
        # simulate both attributes
        self.content = text
        self.parts = [SimpleNamespace(text=text)]
        self.user_id = "u"
        self.session_id = "s"
    def __str__(self):
        return self.content


def setup_dummy_runs(orch, custom_response, search_response):
    async def custom_run(ctx):
        yield DummyEvent(custom_response)
    async def search_run(ctx):
        yield DummyEvent(search_response)
    orch._custom = SimpleNamespace(run_async=custom_run)
    orch._search = SimpleNamespace(run_async=search_run)


def test_routing_horse():
    orch = SmartOrchestrator()
    setup_dummy_runs(orch, "custom response", "search response")
    ctx = DummyCtx("I love Horses!")
    results = collect(orch._run_async_impl(ctx))
    assert any(evt.content == "custom response" for evt in results)


def test_routing_dice():
    orch = SmartOrchestrator()
    setup_dummy_runs(orch, "dice response", "search response")
    ctx = DummyCtx("Please roll a DICE.")
    results = collect(orch._run_async_impl(ctx))
    assert any(evt.content == "dice response" for evt in results)


def test_routing_search():
    orch = SmartOrchestrator()
    setup_dummy_runs(orch, "custom response", "search response")
    ctx = DummyCtx("What is Python?")
    results = collect(orch._run_async_impl(ctx))
    assert any(evt.content == "search response" for evt in results)


def test_context_fallback():
    orch = SmartOrchestrator()
    setup_dummy_runs(orch, "fallback custom", "fallback search")
    ctx = DummyCtx("Random text without keywords.")
    results = collect(orch._run_async_impl(ctx))
    assert any(evt.content == "fallback search" for evt in results)


def test_create_horse_fact_randomness():
    seen = {create_horse_fact() for _ in range(50)}
    expected = {
        "Horses cannot sleep.",
        "Horses have a unique way of communicating with each other through body language.",
        "The fastest recorded speed of a horse is 55 mph (88.5 km/h)."
    }
    assert seen == expected


# # Optionally, test integration of agent_search
# @pytest.mark.asyncio
# async def test_agent_search_run_async(monkeypatch):
#     results = []
#     async def fake_search_run(ctx):
#         yield DummyEvent("search snippet")
#     monkeypatch.setattr(agent_search, 'run_async', fake_search_run)
#     ctx = DummyCtx("Any query.")
#     async for evt in agent_search.run_async(ctx):
#         results.append(evt)
#     assert results and results[0].content == "search snippet"
