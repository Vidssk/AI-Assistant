from datetime import datetime, timezone

SNAPSHOT_VERSION = "1.0"


def collect_meta(*, source: str = "offline", **_kwargs) -> dict:
    return {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "version": SNAPSHOT_VERSION,
        "source": source,
    }
