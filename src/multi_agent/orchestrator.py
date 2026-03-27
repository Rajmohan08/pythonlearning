from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .agents import (
    Agent,
    BuilderAgent,
    CoordinatorAgent,
    CriticAgent,
    PlannerAgent,
    ResearchAgent,
)
from .state import TaskState


@dataclass
class Orchestrator:
    agents: List[Agent]
    rounds: int = 2

    @classmethod
    def default(cls, rounds: int = 2) -> "Orchestrator":
        return cls(
            agents=[
                PlannerAgent(name="planner", role="Plan tasks"),
                ResearchAgent(name="researcher", role="Collect facts"),
                BuilderAgent(name="builder", role="Draft solution"),
                CriticAgent(name="critic", role="Review solution"),
                CoordinatorAgent(name="coordinator", role="Finalize output"),
            ],
            rounds=rounds,
        )

    def run(self, task: str) -> TaskState:
        state = TaskState(task=task)
        for _ in range(self.rounds):
            for agent in self.agents:
                agent.step(state)
        return state
