#!/usr/bin/env python3
"""
fitgraph_complete_integratio.py
Improved, safe demo integrating MemVerge (MemMachine) + Neo4j.
- Loads credentials from environment variables (no secrets in code).
- Simulates MemMachine when LIVE_MEMMACHINE not set.
- Minimal, robust error handling.
"""

import os
import sys
import json
import argparse
import requests
from neo4j import GraphDatabase, basic_auth

# -----------------------
# Optional .env loading
# -----------------------
# If python-dotenv is installed and a .env file exists, load it. This is optional
# and will not cause the script to fail if dotenv isn't available.
try:
    from dotenv import load_dotenv
    _ = load_dotenv()  # loads .env into environment if present
except Exception:
    # dotenv not installed or failed: that's ok — rely on environment variables
    pass


# -----------------------
# Configuration (ENV)
# -----------------------
# Use explicit environment variable names. Defaults are provided where sensible.
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://57236897.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # REQUIRED: set in environment

MEMVERGE_API_URL = os.getenv("MEMVERGE_API_URL", "https://api.memverge.com/v1/memory")
MEMVERGE_API_KEY = os.getenv("MEMVERGE_API_KEY")  # OPTIONAL: set to use real API
LIVE_MEMMACHINE = os.getenv("LIVE_MEMMACHINE", "false").lower() in ("1", "true", "yes")


def ensure_password():
    if not NEO4J_PASSWORD:
        print("ERROR: NEO4J_PASSWORD must be set in environment. Exiting.")
        sys.exit(1)

# -----------------------
# MemMachine client
# -----------------------
class MemMachineClient:
    """
    Minimal MemMachine client. If LIVE_MEMMACHINE is False or no API key present,
    the client returns simulated insights to allow offline demos.
    """
    def __init__(self, api_url, api_key, live=False):
        self.url = api_url.rstrip("/")
        self.api_key = api_key
        self.live = live and bool(api_key)
        self.headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    def process_feedback(self, user_id, text):
        payload = {"user_id": user_id, "text": text}
        if self.live:
            try:
                resp = requests.post(f"{self.url}/add", json=payload, headers=self.headers, timeout=8)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                print(f"[MEMMACHINE ERROR] live API call failed: {e}. Falling back to simulated response.")
        # Simulated/Deterministic response for demo purposes
        txt = (text or "").lower()
        if "shoulder" in txt or "shoulders" in txt:
            return {"detected_constraint": "Broad Shoulders", "confidence": 0.98}
        if "back" in txt:
            return {"detected_constraint": "Broad Back", "confidence": 0.95}
        return {"detected_constraint": "Unknown", "confidence": 0.0}

# -----------------------
# Neo4j client
# -----------------------
class Neo4jMemory:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))
        except Exception as e:
            raise RuntimeError(f"Failed to create Neo4j driver: {e}")

    def close(self):
        try:
            if hasattr(self, "driver") and self.driver:
                self.driver.close()
        except Exception:
            pass

    def init_db(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            session.run("""
                MERGE (p1:Product {id: 'zara_blazer_001'})
                SET p1 += {name: 'Zara Structured Blazer', category: 'Blazer', fit: 'Slim', brand: 'Zara', size: 'M'}
                MERGE (p2:Product {id: 'hm_jacket_002'})
                SET p2 += {name: 'HM Slim Fit Jacket', category: 'Blazer', fit: 'Slim', brand: 'H&M', size: 'M'}
            """)
            print("[NEO4J] Initialized catalog with sample products.")

    def save_learned_constraint(self, user_id, product_id, constraint):
        with self.driver.session() as session:
            session.run("""
                MERGE (u:User {id: $uid})
                MERGE (p:Product {id: $pid})
                MERGE (a:BodyAttribute {name: $attr})
                MERGE (u)-[:RETURNED {reason: 'Feedback Processed by MemMachine'}]->(p)
                MERGE (u)-[:HAS_CONSTRAINT]->(a)
            """, uid=user_id, pid=product_id, attr=constraint)
            print(f"[NEO4J] Saved constraint '{constraint}' for user '{user_id}' and product '{product_id}'.")

    def check_fit_risk(self, user_id, product_id):
        with self.driver.session() as session:
            record = session.run("""
                MATCH (u:User {id: $uid})-[:HAS_CONSTRAINT]->(attr:BodyAttribute)
                MATCH (p:Product {id: $pid})
                WHERE p.fit = 'Slim' AND (attr.name CONTAINS 'Broad')
                RETURN p.name AS product, attr.name AS conflict
                LIMIT 1
            """, uid=user_id, pid=product_id).single()
            if record:
                return f"⚠️ STOP! FitGraph recalls you have '{record['conflict']}'. This item ('{record['product']}') is likely too slim."
            return "✅ Green light! Fits your profile."

# -----------------------
# Orchestrator (main)
# -----------------------
def main():
    parser = argparse.ArgumentParser(description="Run FitGraph demo (MemMachine + Neo4j).")
    parser.add_argument("--auto", "-a", action="store_true", help="Run non-interactively, skip prompts")
    parser.add_argument("--yes", "-y", action="store_true", help="Alias for --auto")
    args = parser.parse_args()

    # Validate we have the critical secrets / env vars
    ensure_password()

    auto_mode = args.auto or args.yes

    def wait_prompt(prompt_text: str):
        """Wait for user to press ENTER unless auto_mode is enabled."""
        if auto_mode:
            print(f"{prompt_text} [auto]")
            return
        try:
            input(prompt_text)
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            sys.exit(1)

    neo4j_db = None
    try:
        neo4j_db = Neo4jMemory(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        mem_machine = MemMachineClient(MEMVERGE_API_URL, MEMVERGE_API_KEY, live=LIVE_MEMMACHINE)

        user = "user_123"

        print("\n=== FITGRAPH: MemMachine + Neo4j Demo ===")

        wait_prompt("\n[1] Press ENTER to initialize the database...")
        neo4j_db.init_db()

        wait_prompt("\n[2] Press ENTER to simulate user return and process feedback...")
        raw_feedback = "I'm returning this Zara blazer because it's too tight on my shoulders."

        insight = mem_machine.process_feedback(user, raw_feedback)
        print(f"[MEMMACHINE] Insight: {json.dumps(insight)}")

        if insight and insight.get("confidence", 0) > 0.8:
            constraint = insight.get("detected_constraint", "Unknown")
            neo4j_db.save_learned_constraint(user, "zara_blazer_001", constraint)
            print(f"[AGENT] Stored constraint: {constraint}")
        else:
            print("[AGENT] No high-confidence insight extracted; nothing stored.")

        wait_prompt("\n[3] Press ENTER to simulate shopping for H&M jacket...")
        risk = neo4j_db.check_fit_risk(user, "hm_jacket_002")
        print(f"\n[AGENT] {risk}")

    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if neo4j_db:
            neo4j_db.close()

if __name__ == "__main__":
    main()