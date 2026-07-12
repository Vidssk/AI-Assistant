import argparse
import sys
from pathlib import Path

from export.snapshot import export_snapshot
from export.validate import SnapshotValidationError

DEMO_SNAPSHOT_PATH = Path("snapshots") / "demo.json"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Refresh the canonical demo snapshot used for frontend offline fallback."
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Skip live HTTP fetch and assemble dashboard data from SQLite + system metrics",
    )
    args = parser.parse_args()

    try:
        written_path = export_snapshot(
            DEMO_SNAPSHOT_PATH,
            prefer_live=not args.offline,
            validate=True,
        )
    except SnapshotValidationError as error:
        print("Snapshot validation failed:", file=sys.stderr)
        for message in error.errors:
            print(f"  - {message}", file=sys.stderr)
        raise SystemExit(1) from error

    print(f"Demo snapshot written to {written_path.resolve()}")


if __name__ == "__main__":
    main()
