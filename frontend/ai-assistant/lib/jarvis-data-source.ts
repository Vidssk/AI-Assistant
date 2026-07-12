import { applyPayload, parsePayload } from "./jarvis-payload";
import type { JarvisData, JarvisPayload, JarvisSource } from "./jarvis-types";

const WS_URL =
  process.env.NEXT_PUBLIC_JARVIS_WS_URL ?? "ws://127.0.0.1:8000/ws";
const SNAPSHOT_URL =
  process.env.NEXT_PUBLIC_SNAPSHOT_URL ?? "/snapshot.json";
const CONNECT_TIMEOUT_MS = 3000;
const RECONNECT_INTERVAL_MS = Number(
  process.env.NEXT_PUBLIC_JARVIS_RECONNECT_MS ?? 5000
);

export type Unsubscribe = () => void;

export const initialData = (): JarvisData => ({
  status: "connecting...",
  agent: null,
  events: [],
  system: null,
  connected: false,
  source: "connecting",
  error: null,
});

function hasContent(data: JarvisData): boolean {
  return data.events.length > 0 || data.system !== null || data.agent !== null;
}

function eventsEqual(a: JarvisData["events"], b: JarvisData["events"]): boolean {
  if (a === b) return true;
  if (a.length !== b.length) return false;
  return a.every(
    (entry, i) =>
      entry.timestamp === b[i].timestamp && entry.event === b[i].event
  );
}

function systemEqual(
  a: JarvisData["system"],
  b: JarvisData["system"]
): boolean {
  if (a === b) return true;
  if (a === null || b === null) return a === b;
  return JSON.stringify(a) === JSON.stringify(b);
}

function isSameData(a: JarvisData, b: JarvisData): boolean {
  return (
    a.status === b.status &&
    a.agent === b.agent &&
    a.connected === b.connected &&
    eventsEqual(a.events, b.events) &&
    systemEqual(a.system, b.system) &&
    a.source === b.source &&
    a.error === b.error
  );
}

export function subscribeJarvisData(
  onChange: (data: JarvisData) => void
): Unsubscribe {
  let data = initialData();
  let mode: JarvisSource = "connecting";
  let ws: WebSocket | null = null;
  let connectTimeout: ReturnType<typeof setTimeout> | null = null;
  let reconnectTimer: ReturnType<typeof setInterval> | null = null;
  let snapshotAbort: AbortController | null = null;
  let connectGeneration = 0;
  let silentAttemptInFlight = false;
  let disposed = false;

  const emit = (next: Partial<JarvisData>) => {
    const merged: JarvisData = {
      ...data,
      ...next,
      source: next.source ?? mode,
    };
    if (isSameData(data, merged)) return;
    data = merged;
    onChange(data);
  };

  const clearConnectTimeout = () => {
    if (connectTimeout !== null) {
      clearTimeout(connectTimeout);
      connectTimeout = null;
    }
  };

  const clearReconnectInterval = () => {
    if (reconnectTimer !== null) {
      clearInterval(reconnectTimer);
      reconnectTimer = null;
    }
  };

  const closeWebSocket = () => {
    if (ws) {
      ws.onopen = null;
      ws.onmessage = null;
      ws.onerror = null;
      ws.onclose = null;
      ws.close();
      ws = null;
    }
  };

  const scheduleReconnect = () => {
    if (disposed || mode !== "snapshot") return;
    clearReconnectInterval();
    reconnectTimer = setInterval(() => {
      if (!disposed && mode === "snapshot" && !silentAttemptInFlight) {
        tryConnect({ silent: true });
      }
    }, RECONNECT_INTERVAL_MS);
  };

  const reportSnapshotError = (message: string) => {
    console.error(message);
    if (!hasContent(data)) {
      emit({ error: "Data feed unavailable — retrying..." });
    }
  };

  const loadSnapshot = async (abort: AbortController) => {
    try {
      const response = await fetch(SNAPSHOT_URL, { signal: abort.signal });
      if (!response.ok) {
        reportSnapshotError(`Failed to load snapshot: ${response.status}`);
        return;
      }

      const json: unknown = await response.json();
      const payload = parsePayload(json);
      if (!payload) {
        reportSnapshotError("Failed to parse snapshot payload");
        return;
      }

      if (disposed || mode !== "snapshot" || abort.signal.aborted) return;

      emit({
        ...applyPayload(payload, data),
        connected: false,
        error: null,
      });
    } catch (error) {
      if (abort.signal.aborted) return;
      reportSnapshotError(`Failed to fetch snapshot: ${error}`);
    }
  };

  const enterSnapshot = () => {
    if (disposed) return;

    const alreadyInSnapshot = mode === "snapshot";

    snapshotAbort?.abort();
    mode = "snapshot";
    clearConnectTimeout();
    closeWebSocket();

    if (!alreadyInSnapshot) {
      emit({ connected: false, source: "snapshot" });
    }

    if (!hasContent(data)) {
      const abort = new AbortController();
      snapshotAbort = abort;
      void loadSnapshot(abort);
    }

    if (!alreadyInSnapshot) {
      scheduleReconnect();
    }
  };

  const enterLive = (payload?: JarvisPayload) => {
    if (disposed) return;

    mode = "live";
    silentAttemptInFlight = false;
    clearConnectTimeout();
    clearReconnectInterval();
    snapshotAbort?.abort();
    snapshotAbort = null;

    if (payload) {
      emit({ ...applyPayload(payload, data), connected: true, error: null });
    } else {
      emit({ connected: true, error: null });
    }
  };

  const tryConnect = (options?: { silent?: boolean }) => {
    if (disposed || mode === "live") return;

    const silent = options?.silent ?? false;
    const generation = ++connectGeneration;
    clearConnectTimeout();
    closeWebSocket();

    if (silent) {
      silentAttemptInFlight = true;
    } else {
      mode = "connecting";
      emit({ source: "connecting", error: null });
    }

    ws = new WebSocket(WS_URL);

    const abandonSilentAttempt = () => {
      if (disposed || generation !== connectGeneration) return;
      clearConnectTimeout();
      closeWebSocket();
      silentAttemptInFlight = false;
    };

    connectTimeout = setTimeout(() => {
      if (disposed || generation !== connectGeneration) return;
      if (silent) {
        abandonSilentAttempt();
        return;
      }
      if (mode !== "connecting") return;
      enterSnapshot();
    }, CONNECT_TIMEOUT_MS);

    ws.onopen = () => {
      if (disposed || generation !== connectGeneration) return;
      silentAttemptInFlight = false;
      enterLive();
    };

    ws.onmessage = (event) => {
      if (disposed || mode !== "live") return;
      try {
        const parsed: unknown = JSON.parse(event.data);
        const payload = parsePayload(parsed);
        if (!payload) return;
        emit({ ...applyPayload(payload, data), connected: true, error: null });
      } catch {
        console.error("Failed to parse WS message:", event.data);
      }
    };

    ws.onerror = () => {
      if (disposed || generation !== connectGeneration) return;
      if (silent) {
        abandonSilentAttempt();
        return;
      }
      if (mode !== "connecting") return;
      clearConnectTimeout();
      enterSnapshot();
    };

    ws.onclose = () => {
      if (disposed || generation !== connectGeneration) return;
      clearConnectTimeout();
      if (silent) return;
      if (mode === "live") {
        enterSnapshot();
      } else if (mode === "connecting") {
        enterSnapshot();
      }
    };
  };

  emit(data);
  tryConnect();

  return () => {
    disposed = true;
    clearConnectTimeout();
    clearReconnectInterval();
    snapshotAbort?.abort();
    snapshotAbort = null;
    closeWebSocket();
  };
}
