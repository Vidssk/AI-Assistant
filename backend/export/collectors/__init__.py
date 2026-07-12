from export.collectors.dashboard import collect_dashboard
from export.collectors.meta import collect_meta
from export.collectors.persisted import collect_persisted

COLLECTORS = {
    "meta": collect_meta,
    "dashboard": collect_dashboard,
    "persisted": collect_persisted,
}
