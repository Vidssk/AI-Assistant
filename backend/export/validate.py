def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_string(value) -> bool:
    return isinstance(value, str)


def _is_string_or_null(value) -> bool:
    return value is None or isinstance(value, str)


def _is_number_or_null(value) -> bool:
    return value is None or _is_number(value)


class SnapshotValidationError(Exception):
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("\n".join(errors))


def validate_snapshot(data: dict) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["snapshot must be a JSON object"]

    _validate_meta(data.get("meta"), errors)
    _validate_dashboard(data.get("dashboard"), errors)
    _validate_persisted(data.get("persisted"), errors)

    return errors


def _validate_meta(meta, errors: list[str]) -> None:
    if not isinstance(meta, dict):
        errors.append("meta must be an object")
        return

    for field in ("exported_at", "version", "source"):
        value = meta.get(field)
        if not _is_string(value):
            errors.append(f"meta.{field} must be a string")


def _validate_dashboard(dashboard, errors: list[str]) -> None:
    if not isinstance(dashboard, dict):
        errors.append("dashboard must be an object")
        return

    status = dashboard.get("status")
    if not _is_string(status):
        errors.append("dashboard.status must be a string")

    if "agent" not in dashboard:
        errors.append("dashboard.agent is required")
    elif not _is_string_or_null(dashboard.get("agent")):
        errors.append("dashboard.agent must be a string or null")

    events = dashboard.get("events")
    if events is not None:
        if not isinstance(events, list):
            errors.append("dashboard.events must be an array")
        else:
            for index, event in enumerate(events):
                _validate_event(event, f"dashboard.events[{index}]", errors)

    system = dashboard.get("system")
    if system is not None:
        _validate_system(system, "dashboard.system", errors)


def _validate_event(event, path: str, errors: list[str]) -> None:
    if not isinstance(event, dict):
        errors.append(f"{path} must be an object")
        return

    if not _is_string(event.get("timestamp")):
        errors.append(f"{path}.timestamp must be a string")
    if not _is_string(event.get("event")):
        errors.append(f"{path}.event must be a string")


def _validate_system(system, path: str, errors: list[str]) -> None:
    if not isinstance(system, dict):
        errors.append(f"{path} must be an object or null")
        return

    cpu = system.get("cpu")
    if not isinstance(cpu, dict):
        errors.append(f"{path}.cpu must be an object")
    else:
        if not _is_number(cpu.get("usage")):
            errors.append(f"{path}.cpu.usage must be a number")
        if not _is_number_or_null(cpu.get("temperature")):
            errors.append(f"{path}.cpu.temperature must be a number or null")

    gpu = system.get("gpu")
    if not isinstance(gpu, dict):
        errors.append(f"{path}.gpu must be an object")
    else:
        if not _is_string_or_null(gpu.get("name")):
            errors.append(f"{path}.gpu.name must be a string or null")
        for field in ("usage", "temperature", "vram_used", "vram_total"):
            if not _is_number(gpu.get(field)):
                errors.append(f"{path}.gpu.{field} must be a number")

    memory = system.get("memory")
    if not isinstance(memory, dict):
        errors.append(f"{path}.memory must be an object")
    else:
        for field in ("used", "total"):
            if not _is_number(memory.get(field)):
                errors.append(f"{path}.memory.{field} must be a number")


def _validate_persisted(persisted, errors: list[str]) -> None:
    if not isinstance(persisted, dict):
        errors.append("persisted must be an object")
        return

    state = persisted.get("state")
    if not isinstance(state, dict):
        errors.append("persisted.state must be an object")

    events = persisted.get("events")
    if not isinstance(events, list):
        errors.append("persisted.events must be an array")
    else:
        for index, event in enumerate(events):
            _validate_event(event, f"persisted.events[{index}]", errors)
