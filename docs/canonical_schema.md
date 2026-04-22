Tables


Table: dim_time
Purpose: canonical monthly time dimension.


time_id (PK, date): first day of month (e.g. 2026-03-01)
year (int, 4-digit)
month (int, 1–12)
period_start (date): same as time_id
period_end (date): last day of month


Constraints  
Unique time_id
time_id must always be the first of the month.


Table: dim_geo
Purpose: canonical geography dimension supporting national, state, and FMMO order geographies.
geo_id (PK, string)
National: US
State: US-STATE-CA, US-STATE-WI, …
FMMO: US-FMMO-ORDER-001, US-FMMO-ORDER-124, …
geo_level (enum): national | state | fmmo_order
scheme (string)
National: NATIONAL
State: USPS_STATE
FMMO: USDA_FMMO_ORDER
code (string, nullable)
State: state abbreviation (CA)
FMMO: order number as string ("1", "124")
name (string)
State full name, or FMMO order name (e.g. Northeast)
parent_geo_id (string, FK → dim_geo.geo_id, nullable)
Recommended: all states and FMMO orders have parent US
fips (string, nullable; states only)
state_abbr (string, nullable; states only)
Constraints

Unique geo_id
Unique (scheme, code) where code is not null
geo_level and scheme must be consistent:
national → NATIONAL
state → USPS_STATE
fmmo_order → USDA_FMMO_ORDER
Interpretation rule

“All Markets Combined” from AMS FMMO reports is stored as national with geo_id = US.


Table: dim_entity
Purpose: identifies who the series belongs to (USDA vs user).


entity_id (PK, string or uuid)
entity_type (enum): usda | user
display_name (string)
owner_user_id (string/uuid, nullable; required for entity_type=user)
default_geo_id (string, FK → dim_geo.geo_id, nullable)
metadata_json (json, nullable)


Table: dim_metric
Purpose: defines the meaning and expected unit/behavior of an observation.

metric_id (PK, string, snake_case)
name (string)
description (string, nullable)
domain (enum): milk | feed | herd | finance | other
base_unit (string) from unit vocabulary
value_type (enum): quantity | price | count | percent | ratio | index
aggregation (enum): avg | sum | end_of_month | none


FMMO metric set  
producer_milk_receipts (unit million_lb, value_type quantity, aggregation sum)
producer_butterfat (unit percent, value_type percent, aggregation none)
producer_nonfat_solids (unit percent, aggregation none)
producer_true_protein (unit percent, aggregation none)
producer_other_solids (unit percent, aggregation none)
producer_scc (unit thousand_cells_per_ml, aggregation none)


Table: metric_geo_availability
Purpose: drives frontend filtering (Option B UX): only show geographies valid for the selected metric.

metric_id (FK → dim_metric.metric_id)
geo_level (enum): national | state | fmmo_order
scheme (string, nullable)
    Required when geo_level=fmmo_order → USDA_FMMO_ORDER
    Null for national and typically for state
is_default (bool)


Constraints  
Unique (metric_id, geo_level, scheme)
Exactly one is_default=true row per metric_id (recommended)


FMMO availability (v1) For each of the 6 FMMO metrics:
(fmmo_order, scheme USDA_FMMO_ORDER, is_default=true)
(national, scheme null, is_default=false)


dataset
Purpose: registry of ingestible datasets (USDA sources and user uploads).

dataset_id (PK, string or uuid)
dataset_type (enum): usda | user_upload
name (string)
provider (string, nullable)
refresh_cadence (enum): daily | weekly | monthly | quarterly | annual | ad_hoc
raw_uri (string, nullable)
notes (string, nullable)


dataset_run
Purpose: lineage of each ingestion execution.

run_id (PK, uuid)
dataset_id (FK → dataset.dataset_id)
status (enum): started | succeeded | failed
started_at (timestamp)
finished_at (timestamp, nullable)
stats_json (json, nullable)
error_json (json, nullable)
code_version (string, nullable) (git SHA)


fact_observation
Purpose: canonical time-series fact table.


observation_id (PK, uuid)
metric_id (FK → dim_metric.metric_id)
time_id (FK → dim_time.time_id)
geo_id (FK → dim_geo.geo_id)
entity_id (FK → dim_entity.entity_id)
value (numeric)
unit (string) from unit vocabulary (must be compatible with dim_metric.base_unit)
source (enum): usda | user_upload | derived (use derived later if you add stored KPIs)
dataset_id (FK → dataset.dataset_id, nullable)
run_id (FK → dataset_run.run_id, nullable)
source_series_id (string, nullable) (e.g. USDA series code if applicable)
quality_flag (enum, nullable): ok | estimated | suppressed | outlier
ingested_at (timestamp)


Constraints  
Unique (metric_id, time_id, geo_id, entity_id)
unit must be in unit vocabulary
time_id must be monthly (first of month)

Units vocabulary  
million_lb
percent
thousand_cells_per_ml
