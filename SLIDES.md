FitGraph — 3-slide pitch

Slide 1 — Title
FitGraph — Smarter Fit Warnings
One-line: Convert user return feedback into explainable fit warnings using a small inference module + graph storage.

Slide 2 — Problem & Solution
Problem: High return rates from poor fit; shoppers lack personalized fit guidance.
Solution: Capture user feedback ("too tight on shoulders"), infer body attribute (e.g., Broad Shoulders), store as graph facts (Neo4j), and warn on products likely to conflict.

Slide 3 — Demo & Ask
Demo steps:
- Start local Neo4j: `docker run -d --name fitgraph-neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/fitgraph_test_pass neo4j:5`
- Run demo: `./present.sh` (creates `fitgraph_demo_output.txt` and `fitgraph_demo_results.json` on the Desktop)

Ask: Judges — feedback on where to partner next (data access, UX integration) or potential pilot opportunities.
