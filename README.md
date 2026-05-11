# Databricks Asset Bundles — Insurance DLT Pipeline CI/CD

✅ **Status:** Complete — DLT pipeline deployed as Infrastructure as Code via Databricks Asset Bundles (May 2026).

## What This Project Demonstrates

This project takes the Insurance DLT Pipeline (built in [insurance-dlt-pipeline](https://github.com/Shishubala-01/insurance-dlt-pipeline)) and makes it **deployable as code**. Instead of creating pipelines manually in the Databricks UI, the pipeline configuration is defined in YAML and deployed via the Databricks CLI.

### The Problem This Solves

In production data engineering, pipelines created manually in a UI are:
- **Not reproducible** — if someone deletes the pipeline, you recreate it from memory
- **Not reviewable** — config changes happen silently, with no audit trail
- **Not portable** — moving to a new workspace means clicking through the same screens again
- **Not testable** — no way to validate config before deploying

### The Solution

Databricks Asset Bundles define pipeline configuration as YAML files stored in Git:
- **Reproducible** — databricks bundle deploy recreates the pipeline in 30 seconds
- **Reviewable** — config changes go through Git PRs with full diff visibility
