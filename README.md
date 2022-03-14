# f1-lineup-optimization-api
Uses linear programming (PuLP and GLPK) to solve for optimal F1 lineups.

Deployed as a REST API on GCP with CloudRun [here](https://almanac-ol22472xua-uk.a.run.app/redoc).

It will likely take ~5 seconds to load from a cold start since the minimum instances is currently set to 0.
