Multi-Agent AI System (Python + Docker)

Overview
This sample project simulates a multi-agent AI system using local heuristics. It includes planner, researcher, builder, critic, and coordinator agents that collaborate on a task without external APIs.

What is included
- A small multi-agent orchestration loop
- Deterministic, local agents (no network calls)
- Dockerfile and docker-compose for containerized runs

Local run
1) Create and activate a Python environment
2) Run the app with a task
   Example (Windows PowerShell):
   set PYTHONPATH=src
   python -m multi_agent.app --task "Design a build and deploy flow" --rounds 2

Docker run
1) Build the image
   docker build -t multi-agent-sample .
2) Run the container
   docker run --rm multi-agent-sample

Docker Compose
1) Build and run
   docker compose up --build

Notes
- This project uses standard library only
- Replace the sample task with your own prompt
