"""Load and serve the Fleet / Rack / Tier registry (including BIAN maps)."""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

import yaml

from src.fleet.models import Fleet, FleetRegistry, FleetStatus, Rack, Tier

logger = logging.getLogger(__name__)

DEFAULT_REGISTRY_PATH = Path(__file__).resolve().parents[2] / "config" / "fleets" / "registry.yaml"


def _load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@lru_cache(maxsize=1)
def get_registry(path: Optional[str] = None) -> FleetRegistry:
    p = Path(path) if path else DEFAULT_REGISTRY_PATH
    if not p.exists():
        logger.warning("Fleet registry not found at %s – empty registry", p)
        return FleetRegistry(fleets=[])
    data = _load_yaml(p)
    extra_paths = []
    be = p.parent / "banking_extensions.yaml"
    if be.exists():
        extra_paths.append(be)
    ext_dir = p.parent / "extensions"
    if ext_dir.is_dir():
        extra_paths.extend(sorted(ext_dir.glob("*.yaml")))
    for ep in extra_paths:
        extra = _load_yaml(ep)
        extra_fleets = extra.get("fleets") if isinstance(extra, dict) else None
        if extra_fleets:
            data.setdefault("fleets", []).extend(extra_fleets)
            logger.info("Merged %d fleets from %s", len(extra_fleets), ep)

    merged_raw: dict = {}
    order: List[str] = []
    for raw in data.get("fleets", []):
        if not isinstance(raw, dict):
            continue
        fid = raw.get("fleet_id")
        if not fid:
            continue
        if fid not in merged_raw:
            merged_raw[fid] = dict(raw)
            merged_raw[fid]["racks"] = list(raw.get("racks") or [])
            merged_raw[fid]["tiers"] = list(raw.get("tiers") or [])
            order.append(fid)
        else:
            existing = merged_raw[fid]
            seen_r = {r.get("rack_id") for r in existing.get("racks") or [] if isinstance(r, dict)}
            seen_t = {t.get("tier_id") for t in existing.get("tiers") or [] if isinstance(t, dict)}
            for r in raw.get("racks") or []:
                if isinstance(r, dict) and r.get("rack_id") not in seen_r:
                    existing.setdefault("racks", []).append(r)
                    seen_r.add(r.get("rack_id"))
            for t in raw.get("tiers") or []:
                if isinstance(t, dict) and t.get("tier_id") not in seen_t:
                    existing.setdefault("tiers", []).append(t)
                    seen_t.add(t.get("tier_id"))
            logger.info("Deep-merged racks/tiers into fleet_id=%s from extension", fid)

    fleets: List[Fleet] = []
    for fid in order:
        raw = merged_raw[fid]
        racks = [Rack(**r) for r in raw.pop("racks", []) if isinstance(r, dict)]
        tiers = [Tier(**t) for t in raw.pop("tiers", []) if isinstance(t, dict)]
        status = raw.pop("status", "active")
        fleets.append(
            Fleet(
                racks=racks,
                tiers=tiers,
                status=FleetStatus(status),
                **{k: v for k, v in raw.items() if k not in ("racks", "tiers")},
            )
        )
    reg = FleetRegistry(
        fleets=fleets,
        bian_version_default=str(data.get("bian_version_default", "12")),
    )
    logger.info(
        "Loaded %d fleets (%d banking, ref=%s) from %s",
        len(reg.fleets),
        len(reg.list_banking()),
        reg.reference_fleet().fleet_id if reg.reference_fleet() else None,
        p,
    )
    return reg


def reload_registry() -> FleetRegistry:
    get_registry.cache_clear()
    return get_registry()


def list_fleets() -> List[Fleet]:
    return get_registry().list_active()


def get_fleet(fleet_id: str) -> Optional[Fleet]:
    return get_registry().get(fleet_id)


def get_rack(fleet_id: str, rack_id: str) -> Optional[Rack]:
    fleet = get_fleet(fleet_id)
    if not fleet:
        return None
    return fleet.rack(rack_id)


def get_tier(fleet_id: str, tier_id: str) -> Optional[Tier]:
    fleet = get_fleet(fleet_id)
    if not fleet:
        return None
    return fleet.tier(tier_id)


def bian_domains_for(fleet_id: str, rack_id: Optional[str] = None) -> List[str]:
    fleet = get_fleet(fleet_id)
    if not fleet:
        return []
    return fleet.bian_domains_for_rack(rack_id)
