"""Utilities for LangChain configuration."""

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


def default_memory() -> ConversationBufferMemory:
    """Return a basic conversation memory."""
    return ConversationBufferMemory()


def simple_prompt_template() -> PromptTemplate:
    """Return a minimal prompt template used across agents."""
    template = "You are a helpful assistant for financial tasks.\n{input}"
    return PromptTemplate.from_template(template)
