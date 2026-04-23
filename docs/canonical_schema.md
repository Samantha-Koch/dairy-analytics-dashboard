Tables


Table: dim_time
Purpose: canonical time dimension supporting annual, quarterly, and monthly grains.

time_id (PK, string): canonical period key
  - year:    "YYYY"  
  - quarter: "YYYY-QN"   
  - month:   "YYYY-MM"  

period_type (enum): year | quarter | month
year (int, 4-digit)
quarter (int, 1–4, nullable; required when period_type=quarter)
month (int, 1–12, nullable; required when period_type=month)
period_start (date)
period_end (date)

Constraints
- Unique time_id
- (period_type, year, quarter, month) must be unique
- quarter must be null unless period_type=quarter
- month must be null unless period_type=month
- period_start and period_end must match the grain:
  - year:    start = YYYY-01-01, end = YYYY-12-31
  - quarter: start/end align to calendar quarters
  - month:   start = first day of month, end = last day of month

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

metric_id (PK, string, snake_case) : globally-unique canonical metric identifier
Naming convention (required)
- For raw ingested metrics, metric_id MUST be namespaced to avoid collisions:
  - <dataset_slug>__<source_data_item>
  - Or when needed: <dataset_slug>__<source_category>__<source_data_item>

name (string)
allowed_period_types (text[], required), allowed values in {year, quarter, month}
description (string, nullable)
domain (enum): milk | feed | herd | finance | other
base_unit (string) from unit vocabulary
value_type (enum): quantity | price | count | percent | ratio | index
aggregation (enum): avg | sum | end_of_month | none


Table: metric_source_map
Purpose: map raw dataset fields → canonical metric_id.

dataset_id (FK → dataset.dataset_id)
source_category (string, nullable)
source_data_item (string)      
metric_id (FK → dim_metric.metric_id)

Constraints
- Unique (dataset_id, source_category, source_data_item)
- Unique metric_id (enforced by dim_metric PK)


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
dataset_slug (string, required, unique, snake_case)
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
source_series_id (string, nullable) 
source_category (string, nullable)
source_data_item (string, nullable)
source_period (string, nullable)
quality_flag (enum, nullable): ok | estimated | suppressed | outlier
ingested_at (timestamp)


Constraints  
Unique (metric_id, time_id, geo_id, entity_id)
unit must be in unit vocabulary


Units vocabulary  
million_lb
percent
thousand_cells_per_ml
