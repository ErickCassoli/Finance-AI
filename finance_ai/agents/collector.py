"""Market data collector agent."""

from typing import Any, Dict

from .base import AgentBase


class AgentCollector(AgentBase):
    """Collects stock and options data along with SELIC rate."""

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # TODO: Implement actual data collection logic
        state["collector"] = {
            "data": None,
        }
        return state
