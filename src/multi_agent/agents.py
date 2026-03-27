from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .state import TaskState


@dataclass
class Agent:
    name: str
    role: str

    def step(self, state: TaskState) -> None:
        raise NotImplementedError


class PlannerAgent(Agent):
    def step(self, state: TaskState) -> None:
        if state.plan:
            return
        state.plan = [
            "Define the system goal and agents",
            "Describe agent interaction flow",
            "Outline build and deployment steps",
            "Provide validation checklist",
        ]
        state.add_message(self.name, "Created an initial plan.")


class ResearchAgent(Agent):
    def step(self, state: TaskState) -> None:
        if state.facts:
            return
        state.facts = [
            "Local simulation avoids external dependencies",
            "Containers package runtime and dependencies",
            "Compose can run multi-service stacks",
        ]
        state.add_message(self.name, "Added local facts and constraints.")


class BuilderAgent(Agent):
    def step(self, state: TaskState) -> None:
        draft: List[str] = []
        draft.append("Goal: " + state.task)
        if state.plan:
            draft.append("Plan:")
            draft.extend([f"- {step}" for step in state.plan])
        if state.facts:
            draft.append("Notes:")
            draft.extend([f"- {fact}" for fact in state.facts])
        if state.critiques:
            draft.append("Adjustments:")
            draft.extend([f"- {c}" for c in state.critiques])
        state.draft = draft
        state.add_message(self.name, "Built a draft response.")


class CriticAgent(Agent):
    def step(self, state: TaskState) -> None:
        critique = "Ensure steps are concise and ordered from build to deploy."
        state.critiques = [critique]
        state.add_message(self.name, "Provided a critique.")


class CoordinatorAgent(Agent):
    def step(self, state: TaskState) -> None:
        if not state.draft:
            return
        output = ["Final Output", "="]
        output.extend(state.draft)
        state.final_output = "\n".join(output)
        state.add_message(self.name, "Produced the final output.")
