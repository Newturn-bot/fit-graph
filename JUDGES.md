FitGraph — One-page pitch for hackathon judges

Tagline
Designing smarter fit recommendations by combining user feedback insights with product fit metadata stored in a graph.

Problem
Sizing and fit are the top causes of product returns in apparel e-commerce. Shoppers lack personalized, actionable fit guidance that reflects their unique body attributes and previous returns.

Solution
FitGraph captures high-confidence, user-provided feedback ("too tight on my shoulders") and converts it into structured body-attribute constraints using a lightweight inference module (simulated MemMachine). Those constraints are stored in Neo4j and used to detect fit-risk for catalog items (e.g., flag slim-fit products when a user has "Broad Shoulders"). The system is real-time, explainable (stores the reason), and minimal to run locally or in containerized environments.

Demo flow (what you'll see)
- Initialize a small product catalog in Neo4j.
- Simulate user return feedback; MemMachine returns a high-confidence constraint (e.g., "Broad Shoulders").
- FitGraph stores the attribute and creates relationships between user and product.
- When the user views another product (e.g., H&M Slim Fit Jacket), FitGraph checks the graph and warns if there's a fit conflict.

Why it matters
- Reduces avoidable returns by surfacing fit risks before checkout.
- Lightweight and privacy-preserving: stores only attributed constraints (no raw sensitive PII) and runs locally for demos.
- Explainable: returns user-friendly warnings and reasons (e.g., "likely too slim for your Broad Shoulders").

Tech highlights
- Python 3.11 demo app with small CLI for automation and non-interactive runs.
- Neo4j (graph) for natural relationships and quick conflict queries.
- Simulated MemMachine client (switchable to a live API by setting `MEMVERGE_API_KEY`).
- Docker + docker-compose for reproducible demos; a `demo.sh` helper starts local Neo4j and runs the script.
- Unit tests (pytest) and a simple CI workflow (GitHub Actions) included for reproducibility.

Impact & Next steps
- For the hackathon: a working demo, reproducible locally, with clear signals for judges about data flow and decision logic.
- Short-term: connect to a real MemMachine API, expand attribute taxonomy, and gather simple user-study metrics (A/B test).
- Long-term: integrate with product metadata pipelines and provide UI overlays in product pages to surface fit warnings.

How to evaluate
- Functionality: demo runs end-to-end and warns appropriately when constraints indicate risk.
- Explainability: can the system show why it flagged a product?
- Reproducibility: included Docker/demo scripts, tests, and a clear README.

Contact
- Run the demo: `./demo.sh` (from the Desktop project folder) or follow `README.md` for manual steps.
