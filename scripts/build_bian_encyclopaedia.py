#!/usr/bin/env python3
"""Build BIAN Agentic RAG encyclopaedia under Fleet → Rack → Tier.

Run from repo root:
  python scripts/build_bian_encyclopaedia.py

Writes:
  fleets/bian/<slug>/service_domain.md
  fleets/bian/_standards/ENCYCLOPAEDIA.md
  fleets/bian/_standards/encyclopaedia_index.json
  fleets/bian/_standards/all_domain_titles.txt
  config/fleets/extensions/bian_encyclopaedia.yaml

If this file is incomplete on a clone, restore from your full workspace copy.
"""
from __future__ import annotations
print("Use the full build_bian_encyclopaedia.py from the local futureim-rag-fleet workspace.")
print("It generates ~220 domain docs under fleets/bian/ with Fleet/Rack/Tier taxonomy.")
raise SystemExit("Full generator lives in the complete local scripts/build_bian_encyclopaedia.py")
