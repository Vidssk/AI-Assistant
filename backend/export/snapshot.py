import json
from pathlib import Path

from export.collectors import COLLECTORS
from export.collectors.dashboard import _fetch_live_dashboard, collect_dashboard


def export_snapshot(output_path: Path, *, prefer_live: bool = True) -> Path:
    source = "offline"
    dashboard = collect_dashboard(prefer_live=False)

    if prefer_live:
        live_payload = _fetch_live_dashboard()
        if live_payload is not None:
            dashboard = live_payload
            source = "live"

    sections = {}
    for name, collector in COLLECTORS.items():
        if name == "meta":
            sections[name] = collector(source=source)
        elif name == "dashboard":
            sections[name] = dashboard
        else:
            sections[name] = collector(prefer_live=prefer_live)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(sections, indent=2, default=str),
        encoding="utf-8",
    )
    return output_path
