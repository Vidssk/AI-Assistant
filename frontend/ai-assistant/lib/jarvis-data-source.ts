import { applyPayload, parsePayload } from "./jarvis-payload";
import type { JarvisData, JarvisPayload } from "./jarvis-types";

const WS_URL =
  process.env.NEXT_PUBLIC_JARVIS_WS_URL ?? "ws://127.0.0.1:8000/ws";
const SNAPSHOT_URL =
  process.env.NEXT_PUBLIC_SNAPSHOT_URL ?? "/snapshot.json";
const CONNECT_TIMEOUT_MS = 3000;
const RECONNECT_INTERVAL_MS = Number(
  process.env.NEXT_PUBLIC_JARVIS_RECONNECT_MS ?? 5000
);

type Mode = "connecting" | "live" | "snapshot";

export type Unsubscribe = () => void;

const initialData = (): JarvisData => ({
  status: "connecting...",
  agent: null,
  events: [],
  system: null,
  connected: false,
});

function isSameData(a: JarvisData, b: JarvisData): boolean {
  return (
    a.status === b.status &&
    a.agent === b.agent &&
    a.connected === b.connected &&
    a.events === b.events &&
    a.system === b.system
  );
}

export function subscribeJarvisData(
  onChange: (data: JarvisData) => void
): Unsubscribe {
  let data = initialData();
  let mode: Mode = "connecting";
  let ws: WebSocket | null = null;
  let connectTimeout: ReturnType<typeof setTimeout> | null = null;
  let reconnectTimer: ReturnType<typeof setInterval> | null = null;
  let snapshotAbort: AbortController | null = null;
  let connectGeneration = 0;
  let disposed = false;

  const emit = (next: JarvisData) => {
    if (isSameData(data, next)) return;
    data = next;
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
      if (!disposed && mode === "snapshot") {
        tryConnect();
      }
    }, RECONNECT_INTERVAL_MS);
  };

  const loadSnapshot = async (abort: AbortController) => {
    try {
      const response = await fetch(SNAPSHOT_URL, { signal: abort.signal });
      if (!response.ok) {
        console.error("Failed to load snapshot:", response.status);
        return;
      }

      const json: unknown = await response.json();
      const payload = parsePayload(json);
      if (!payload) {
        console.error("Failed to parse snapshot payload");
        return;
      }

      if (disposed || mode !== "snapshot" || abort.signal.aborted) return;

      emit({
        ...applyPayload(payload, data),
        connected: false,
      });
    } catch (error) {
      if (abort.signal.aborted) return;
      console.error("Failed to fetch snapshot:", error);
    }
  };

  const enterSnapshot = () => {
    if (disposed) return;

    snapshotAbort?.abort();
    mode = "snapshot";
    clearConnectTimeout();
    closeWebSocket();

    emit({ ...data, connected: false });

    const abort = new AbortController();
    snapshotAbort = abort;
    void loadSnapshot(abort);
    scheduleReconnect();
  };

  const enterLive = (payload?: JarvisPayload) => {
    if (disposed) return;

    mode = "live";
    clearConnectTimeout();
    clearReconnectInterval();
    snapshotAbort?.abort();
    snapshotAbort = null;

    if (payload) {
      emit({ ...applyPayload(payload, data), connected: true });
    } else {
      emit({ ...data, connected: true });
    }
  };

  const tryConnect = () => {
    if (disposed || mode === "live") return;

    const generation = ++connectGeneration;
    clearConnectTimeout();
    closeWebSocket();
    mode = "connecting";

    ws = new WebSocket(WS_URL);

    connectTimeout = setTimeout(() => {
      if (disposed || generation !== connectGeneration || mode !== "connecting") {
        return;
      }
      enterSnapshot();
    }, CONNECT_TIMEOUT_MS);

    ws.onopen = () => {
      if (disposed || generation !== connectGeneration) return;
      enterLive();
    };

    ws.onmessage = (event) => {
      if (disposed || mode !== "live") return;
      try {
        const parsed: unknown = JSON.parse(event.data);
        const payload = parsePayload(parsed);
        if (!payload) return;
        emit({ ...applyPayload(payload, data), connected: true });
      } catch {
        console.error("Failed to parse WS message:", event.data);
      }
    };

    ws.onerror = () => {
      if (disposed || generation !== connectGeneration || mode !== "connecting") {
        return;
      }
      clearConnectTimeout();
      enterSnapshot();
    };

    ws.onclose = () => {
      if (disposed || generation !== connectGeneration) return;
      clearConnectTimeout();
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
