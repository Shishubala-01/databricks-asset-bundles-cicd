"""
DQX Data Quality Validation — Insurance Pipeline

This notebook demonstrates how to use Databricks DQX to validate
data quality using externalized YAML rules. It reads from the
Silver insurance claims table and applies DQX checks, producing
_errors and _warnings columns at the row level.

Prerequisites:
  %pip install databricks-labs-dqx

Usage:
  Run this notebook in a Databricks workspace after deploying the
  DLT pipeline. It reads from workspace.default.silver_insurance_claims
  (or workspace.bundle_dev.silver_insurance_claims for bundle-deployed pipelines).

Author: Kumari Shishubala
"""

# COMMAND ----------

# Install DQX (run once per cluster session)
# %pip install databricks-labs-dqx==0.8.0
# %restart_python

# COMMAND ----------

from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient

# Initialise DQX engine
ws_client = WorkspaceClient()
dq_engine = DQEngine(ws_client)

# COMMAND ----------

# Read Silver insurance claims
df_silver = spark.read.table("workspace.bundle_dev.silver_insurance_claims")
print(f"Input rows: {df_silver.count()}")

# COMMAND ----------

# Load quality checks from YAML
# In production, this file would be stored in the workspace via Asset Bundle deployment
# For this demo, we load from a local/workspace path
checks = dq_engine.load_checks_from_local_file("/Workspace/Users/shishubalak6@gmail.com/.bundle/insurance-dlt-bundle/dev/files/quality/dqx_checks.yaml")
checks_list = checks["checks"]

# Validate the checks file itself (meta-validation)
status = dq_engine.validate_checks(checks_list)
print(f"Checks valid: {not status.has_errors}")
if status.has_errors:
    print(f"Errors: {status.errors}")

# COMMAND ----------

# Apply DQX checks — adds _errors and _warnings columns to each row
df_validated = dq_engine.apply_checks(df_silver, checks_list)

# Show summary
total = df_validated.count()
errors = df_validated.filter("size(_errors) > 0").count()
warnings = df_validated.filter("size(_warnings) > 0").count()
clean = df_validated.filter("size(_errors) = 0 AND size(_warnings) = 0").count()

print(f"Total rows:    {total}")
print(f"Rows with errors:   {errors}")
print(f"Rows with warnings: {warnings}")
print(f"Clean rows:         {clean}")

# COMMAND ----------

# Show rows that have quality issues (errors or warnings)
df_issues = df_validated.filter("size(_errors) > 0 OR size(_warnings) > 0")
df_issues.select("age", "bmi", "charges", "region", "smoker", "_errors", "_warnings").show(20, truncate=False)

# COMMAND ----------

# Quarantine pattern — separate clean data from issues
df_clean = df_validated.filter("size(_errors) = 0")
df_quarantine = df_validated.filter("size(_errors) > 0")

print(f"Clean rows (ready for Gold): {df_clean.count()}")
print(f"Quarantined rows (need review): {df_quarantine.count()}")