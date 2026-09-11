# BIAN Agentic RAG Encyclopaedia

Taxonomy: **Fleet → Rack → Tier**

Reference fleet: `bian` | Enterprise common: `enterprise`

## Dual-pull

1. Product: `fleet_id` / `rack_id` / `tier_id` of product fleet
2. BIAN: `fleet_id=bian` + `bian_service_domain` list for scope
3. Merge → prompt / codegen

KYC, auth, documents, fraud use fleet **enterprise**, which maps racks onto encyclopaedia domains under party/risk tiers.

## How knowledge enters RAG

Each service domain has `fleets/bian/<slug>/service_domain.md`.
Seed or GCS upload → chunk → embed → Vector Search.
Dual-pull only retrieves domains **in scope** for the selected Fleet/Rack/Tier (not all 220+ every time).

## Rebuild

```bash
python scripts/build_bian_encyclopaedia.py
python scripts/seed_bian_knowledge.py
```

See `encyclopaedia_index.json` and `all_domain_titles.txt` for the full domain list.
See `config/fleets/extensions/bian_encyclopaedia.yaml` for Tier/Rack maps on fleet `bian`.
