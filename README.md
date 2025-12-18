
# FitGraph demo (MemMachine + Neo4j)

FitGraph is a demo that combines a simulated MemMachine (MemVerge) insight extractor with a Neo4j graph database to store user body-attribute constraints and check fit risk for products. It's designed as a lightweight, reproducible demo you can run locally or in a container for hackathon presentations.

Requirements
- Python 3.8+
- Dependencies in `requirements.txt` (recommended to install in a venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Running
- Non-interactive (recommended for demos or CI):

```bash
# replace with your real password
# from the project root (Desktop in this repo)
NEO4J_URI='neo4j://localhost:7687' NEO4J_PASSWORD='your_password_here' python3 "./fitgraph_complete_integration.py" --auto
```

- Interactive (press ENTER between steps):

```bash
export NEO4J_URI='neo4j://localhost:7687'
export NEO4J_PASSWORD='your_password_here'
python3 "./fitgraph_complete_integration.py"
```

Docker (optional)
- Build and run with docker-compose (Desktop):

```bash
cd ~/Desktop
docker-compose up --build
```

Demo helper
- Use the provided `demo.sh` to start a local Neo4j container and run the demo end-to-end:

```bash
./demo.sh
```

Optional
- Create a `.env` file in the project root with `NEO4J_PASSWORD` (and optionally `NEO4J_URI`) — the script will attempt to load it if `python-dotenv` is installed.

Notes
- The script uses the Neo4j python driver. Ensure your Neo4j instance allows the provided URI and credentials (bolt on 7687 for local container).
- The CLI flags `--init-only`, `--simulate-feedback`, `--check-only`, `--auto` allow fine-grained automation for demos and CI.

Pitch for judges
- See `JUDGES.md` for a one-page pitch, technical choices, and evaluation points for judges.
