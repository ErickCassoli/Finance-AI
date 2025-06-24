"""Base classes for all agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class AgentBase(ABC):
    """Base class to standardize agent interfaces."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the given state and return an updated state."""
        raise NotImplementedError
