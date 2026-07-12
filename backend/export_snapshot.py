import argparse
from datetime import datetime, timezone
from pathlib import Path

from export.snapshot import export_snapshot


def _default_output_path() -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path("snapshots") / f"snapshot-{timestamp}.json"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export the current Jarvis application state to a JSON snapshot."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file path (default: snapshots/snapshot-<timestamp>.json)",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Skip live HTTP fetch and assemble dashboard data from SQLite + system metrics",
    )
    args = parser.parse_args()

    output_path = args.output or _default_output_path()
    written_path = export_snapshot(output_path, prefer_live=not args.offline)
    print(f"Snapshot written to {written_path.resolve()}")


if __name__ == "__main__":
    main()
