"""Construction of the LangGraph connecting all agents."""

from __future__ import annotations

from langgraph.graph import StateGraph, END

from .agents.collector import AgentCollector
from .agents.analyst import AgentAnalyst
from .agents.analyst_filter import AgentAnalystFilter
from .agents.supervisor import AgentSupervisor


class TradingGraph:
    """Encapsulates the LangGraph representing the multi-agent workflow."""

    def __init__(self) -> None:
        self.collector = AgentCollector("collector")
        self.analyst = AgentAnalyst("analyst")
        self.filter = AgentAnalystFilter("filter")
        self.supervisor = AgentSupervisor("supervisor")
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(dict)
        graph.add_node("collector", self.collector.run)
        graph.add_node("analyst", self.analyst.run)
        graph.add_node("filter", self.filter.run)
        graph.add_node("supervisor", self.supervisor.run)

        graph.set_entry_point("collector")
        graph.add_edge("collector", "analyst")
        graph.add_edge("analyst", "filter")
        graph.add_edge("filter", "supervisor")
        graph.add_edge("supervisor", END)
        return graph.compile()

    def run(self, initial_state: dict | None = None) -> dict:
        """Execute the compiled graph starting from the given state."""
        initial_state = initial_state or {}
        return self.graph.invoke(initial_state)
