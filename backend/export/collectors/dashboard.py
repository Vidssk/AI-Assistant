import json
import urllib.error
import urllib.request

from config.config import get_system_info
from db.events_db import get_events
from db.responses_db import get_latest_response, get_recent_responses
from db.state_db import get_state

STATUS_URL = "http://127.0.0.1:8000/status"
DASHBOARD_EVENT_LIMIT = 20
DASHBOARD_RESPONSE_LIMIT = 3


def build_dashboard_payload(status: str, agent, system: dict) -> dict:
    return {
        "status": status,
        "agent": agent,
        "events": get_events(DASHBOARD_EVENT_LIMIT),
        "system": system,
        "response": get_latest_response(),
        "responses": get_recent_responses(DASHBOARD_RESPONSE_LIMIT),
    }


def _fetch_live_dashboard() -> dict | None:
    try:
        with urllib.request.urlopen(STATUS_URL, timeout=2) as response:
            return json.loads(response.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def collect_dashboard(*, prefer_live: bool = True, **_kwargs) -> dict:
    if prefer_live:
        live_payload = _fetch_live_dashboard()
        if live_payload is not None:
            return live_payload

    state = get_state()
    return build_dashboard_payload(
        status=state["status"],
        agent=state["agent"],
        system=get_system_info(),
    )
