"""
Orchestrator — the main LangGraph agent that coordinates the full pipeline.
Flow: SmartRouter → Subagent → Reviewer → Response
"""

import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
import anthropic

from .smart_router import SmartRouter
from .reviewer import Reviewer
from .subagents.art_analyzer import ArtAnalyzerAgent
from .subagents.market_agent import MarketIntelAgent

load_dotenv()


class AgentState(TypedDict):
    user_input: str
    intent: str
    subagent_output: str
    final_response: str
    approved: bool


def route_node(state: AgentState) -> AgentState:
    router = SmartRouter()
    state["intent"] = router.classify(state["user_input"])
    return state


def subagent_node(state: AgentState) -> AgentState:
    intent = state["intent"]
    user_input = state["user_input"]

    if intent == "art_analysis":
        agent = ArtAnalyzerAgent()
        state["subagent_output"] = agent.run(user_input)
    elif intent == "market_intel":
        agent = MarketIntelAgent()
        state["subagent_output"] = agent.run(user_input)
    else:
        state["subagent_output"] = f"[{intent}] No subagent configured yet for this intent."

    return state


def reviewer_node(state: AgentState) -> AgentState:
    reviewer = Reviewer()
    result = reviewer.review(
        user_input=state["user_input"],
        agent_output=state["subagent_output"],
    )
    state["approved"] = result["approved"]
    state["final_response"] = result["response"]
    return state


def should_retry(state: AgentState) -> str:
    return END


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    graph.add_node("router", route_node)
    graph.add_node("subagent", subagent_node)
    graph.add_node("reviewer", reviewer_node)

    graph.set_entry_point("router")
    graph.add_edge("router", "subagent")
    graph.add_edge("subagent", "reviewer")
    graph.add_conditional_edges("reviewer", should_retry)

    return graph.compile()


class Orchestrator:
    def __init__(self):
        self.graph = build_graph()

    def run(self, user_input: str) -> str:
        initial_state = AgentState(
            user_input=user_input,
            intent="",
            subagent_output="",
            final_response="",
            approved=False,
        )
        result = self.graph.invoke(initial_state)
        return result["final_response"]


if __name__ == "__main__":
    orchestrator = Orchestrator()
    response = orchestrator.run("What is the market value trend for Basquiat works in Europe?")
    print(response)
