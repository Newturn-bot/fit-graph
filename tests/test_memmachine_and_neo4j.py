import os
import sys
import json
import pytest

# Ensure the repository root (Desktop) is on sys.path so tests can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fitgraph_complete_integration import MemMachineClient, Neo4jMemory

class DummySession:
    def __init__(self):
        self.runs = []
    def run(self, query, **kwargs):
        self.runs.append((query, kwargs))
        class Rec:
            def single(self):
                return None
        return Rec()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False

class DummyDriver:
    def __init__(self):
        self.session_obj = DummySession()
    def session(self):
        return self.session_obj
    def close(self):
        pass

def test_memmachine_simulation():
    client = MemMachineClient("https://api.memverge.com/v1/memory", None, live=False)
    insight = client.process_feedback("user_1", "Too tight on my shoulders")
    assert isinstance(insight, dict)
    assert insight.get("detected_constraint") == "Broad Shoulders"
    assert insight.get("confidence", 0) > 0.9

def test_neo4j_memory_init_and_check(monkeypatch):
    # Monkeypatch GraphDatabase.driver to return our DummyDriver
    monkeypatch.setattr('fitgraph_complete_integration.GraphDatabase', type('X', (), {'driver': lambda uri, auth: DummyDriver()}))

    neo = Neo4jMemory("bolt://localhost:7687", "neo4j", "pass")
    # Call init_db; should not raise
    neo.init_db()
    # Save a constraint (this will call session.run)
    neo.save_learned_constraint('user_1', 'zara_blazer_001', 'Broad Shoulders')
    # Check fit risk (our dummy returns no record -> green)
    res = neo.check_fit_risk('user_1', 'hm_jacket_002')
    assert "Green light" in res or "Fits your profile" in res
    neo.close()
