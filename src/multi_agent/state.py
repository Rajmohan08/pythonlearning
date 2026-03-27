from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Message:
    agent: str
    content: str


@dataclass
class TaskState:
    task: str
    facts: List[str] = field(default_factory=list)
    plan: List[str] = field(default_factory=list)
    draft: List[str] = field(default_factory=list)
    critiques: List[str] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
    final_output: Optional[str] = None

    def add_message(self, agent: str, content: str) -> None:
        self.messages.append(Message(agent=agent, content=content))
