# BIAN Agentic RAG Encyclopaedia

Taxonomy: **Fleet → Rack → Tier**

- Reference fleet: `bian` (~220 service domains)
- Enterprise common: `enterprise` (KYC, auth, docs, fraud)
- Product fleets dual-pull product policy + BIAN domains for active rack/tier

## Dual-pull

1. Product: `fleet_id` / `rack_id` / `tier_id`
2. BIAN: `fleet_id=bian` + `bian_service_domain` list
3. Merge → prompt / codegen

## Rebuild

```bash
python scripts/build_bian_encyclopaedia.py
python scripts/seed_bian_knowledge.py
```

Full domain list: `all_domain_titles.txt`  
Registry map: `config/fleets/extensions/bian_encyclopaedia.yaml` (regenerate via build script if truncated on remote)
