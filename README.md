# Spotify Recently Played Songs Data Pipeline #
## Overview ##
This project demonstrates a modern, end-to-end data engineering workflow leveraging open-source technologies. The pipeline extracts a user’s recently played tracks from the Spotify API, stores raw data in PostgreSQL, transforms it into analytics-ready models with dbt, and visualizes key insights using Apache Superset. Orchestration and scheduling are managed with Apache Airflow.

Designed with modularity, reproducibility, and scalability in mind, this architecture can easily be extended to other APIs or analytical use cases.

## Architecture ##

  <img width="1160" height="580" alt="Blank diagram (1)" src="https://github.com/user-attachments/assets/b1b5e0cb-8559-4a22-ab9f-af084abfa7a1" />

## Features ##
- Automated Data Extraction – Fetches recently played Spotify tracks using the Spotify Web API.
- Raw & Analytics Layers – Implements a clear data modeling strategy (staging, intermediate, and mart layers in dbt).
- SQL-based Transformations – Uses dbt for modular, version-controlled transformations.
- Interactive Dashboards – Superset provides streaming history analysis and trend insights.
- Orchestration – Airflow DAGs schedule and monitor end-to-end data workflows.
- Containerized Architecture – All services (Airflow, PostgreSQL, Superset, dbt CLI) run inside Docker containers, ensuring consistent environments across development, testing, and production.

## Tech Stack ##
| Component         | Technology      | Purpose                        |
| ----------------- | --------------- | ------------------------------ |
| **Source**        | Spotify Web API | Data extraction                |
| **Storage**       | PostgreSQL      | Raw + analytics storage        |
| **Transform**     | dbt             | Data modeling & transformation |
| **BI**            | Apache Superset | Data visualization             |
| **Orchestration** | Apache Airflow  | Workflow management            |
| **Language**      | Python / SQL    | Core ETL and modeling logic    |

## Design Decisions ##
1. PostgreSQL for Storage
Chosen for its robustness, ACID compliance, and wide community support. Storing both raw and transformed data in the same engine simplifies maintenance while still supporting layered modeling.

2. dbt for Transformation
   - dbt was selected over custom SQL scripts to enable:
   - Version-controlled, modular SQL models.
   - Automated dependency management between transformations.
   - Built-in testing, documentation, and lineage tracking.

3. Airflow for Orchestration
Airflow provides fine-grained scheduling, retry logic, and clear DAG visualization. This makes the pipeline production-ready from day one and ensures easy extension to more data sources or downstream tasks.

4. Superset for BI
Superset offers lightweight, self-service BI without vendor lock-in. It integrates directly with PostgreSQL and supports interactive dashboards.

5. API-Centric Data Source
Using the Spotify Web API demonstrates handling rate limits, authentication, and incremental data pulls—skills directly applicable to enterprise data integrations.

6. Local Development with Docker
Containerization ensures that all services (Airflow, PostgreSQL, Superset) run in consistent environments, enabling seamless deployment to cloud environments.

