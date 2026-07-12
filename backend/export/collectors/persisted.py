from db.events_db import get_events
from db.state_db import get_state


def collect_persisted(**_kwargs) -> dict:
    return {
        "state": get_state(),
        "events": get_events(limit=None),
    }
