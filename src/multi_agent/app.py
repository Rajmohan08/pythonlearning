from __future__ import annotations

import argparse

from .orchestrator import Orchestrator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multi-agent AI system simulation")
    parser.add_argument(
        "--task",
        required=True,
        help="Task prompt for the multi-agent system",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=2,
        help="Number of orchestration rounds",
    )
    parser.add_argument(
        "--transcript",
        action="store_true",
        help="Print agent messages",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    system = Orchestrator.default(rounds=args.rounds)
    state = system.run(task=args.task)

    if args.transcript:
        print("Transcript")
        print("=")
        for message in state.messages:
            print(f"[{message.agent}] {message.content}")
        print()

    if state.final_output:
        print(state.final_output)
    else:
        print("No output generated.")


if __name__ == "__main__":
    main()
