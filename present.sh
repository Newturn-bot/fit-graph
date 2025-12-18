#!/usr/bin/env bash
# present.sh - helper to run demo steps and collect key query results for judges
# Usage: ./present.sh

set -eu
WORKDIR="$(cd "$(dirname "$0")" && pwd)"
OUT="$WORKDIR/fitgraph_demo_output.txt"
JSON_OUT="$WORKDIR/fitgraph_demo_results.json"

echo "Running demo (init -> simulate -> check) and saving stdout to $OUT"
NEO4J_URI='neo4j://localhost:7687' NEO4J_PASSWORD='fitgraph_test_pass' python3 "$WORKDIR/fitgraph_complete_integration.py" --auto | tee "$OUT"

# Small Python snippet to query Neo4j for presentation-friendly JSON results
python3 - <<PY
from neo4j import GraphDatabase
import os, json
uri = os.environ.get('NEO4J_URI','neo4j://localhost:7687')
password = os.environ.get('NEO4J_PASSWORD','fitgraph_test_pass')
driver = GraphDatabase.driver(uri, auth=("neo4j", password))
with driver.session() as session:
    prod = session.run("MATCH (p:Product) RETURN p.id AS id, p.name AS name, p.fit AS fit LIMIT 25").data()
    users = session.run("MATCH (u:User)-[:HAS_CONSTRAINT]->(a:BodyAttribute) RETURN u.id AS user, collect(a.name) AS constraints").data()
    conflict = session.run("MATCH (u:User {id:'user_123'})-[:HAS_CONSTRAINT]->(attr:BodyAttribute), (p:Product {id:'hm_jacket_002'}) WHERE p.fit='Slim' AND attr.name CONTAINS 'Broad' RETURN p.name AS product, attr.name AS conflict LIMIT 5").data()
    out = {'products':prod,'users':users,'conflict':conflict}
    with open('fitgraph_demo_results.json','w') as f:
        json.dump(out,f,indent=2)
    print('Wrote', os.path.abspath('fitgraph_demo_results.json'))
    print(json.dumps(out, indent=2))
driver.close()
PY

echo "Done. Files on Desktop: fitgraph_demo_output.txt and fitgraph_demo_results.json"
