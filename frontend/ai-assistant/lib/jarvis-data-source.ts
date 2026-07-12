import { applyPayload, parsePayload } from "./jarvis-payload";
import type { JarvisData } from "./jarvis-types";

const WS_URL =
  process.env.NEXT_PUBLIC_JARVIS_WS_URL ?? "ws://127.0.0.1:8000/ws";
const SNAPSHOT_URL =
  process.env.NEXT_PUBLIC_SNAPSHOT_URL ?? "/snapshot.json";
const CONNECT_TIMEOUT_MS = 3000;

export type Unsubscribe = () => void;

const initialData = (): JarvisData => ({
  status: "connecting...",
  agent: null,
  events: [],
  system: null,
  connected: false,
});

export function subscribeJarvisData(
  onChange: (data: JarvisData) => void
): Unsubscribe {
  let data = initialData();
  let ws: WebSocket | null = null;
  let connectTimeout: ReturnType<typeof setTimeout> | null = null;
  let opened = false;
  let fallbackUsed = false;
  let disposed = false;

  const emit = (next: JarvisData) => {
    data = next;
    onChange(data);
  };

  const loadSnapshot = async () => {
    if (fallbackUsed || disposed) return;
    fallbackUsed = true;

    try {
      const response = await fetch(SNAPSHOT_URL);
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

      emit({
        ...applyPayload(payload, data),
        connected: false,
      });
    } catch (error) {
      console.error("Failed to fetch snapshot:", error);
    }
  };

  const triggerFallback = () => {
    if (opened || fallbackUsed || disposed) return;
    if (ws) {
      ws.close();
      ws = null;
    }
    void loadSnapshot();
  };

  const clearConnectTimeout = () => {
    if (connectTimeout !== null) {
      clearTimeout(connectTimeout);
      connectTimeout = null;
    }
  };

  emit(data);

  ws = new WebSocket(WS_URL);

  connectTimeout = setTimeout(triggerFallback, CONNECT_TIMEOUT_MS);

  ws.onopen = () => {
    if (disposed) return;
    opened = true;
    clearConnectTimeout();
    emit({ ...data, connected: true });
  };

  ws.onmessage = (event) => {
    if (disposed) return;
    try {
      const parsed: unknown = JSON.parse(event.data);
      const payload = parsePayload(parsed);
      if (!payload) return;
      emit(applyPayload(payload, data));
    } catch {
      console.error("Failed to parse WS message:", event.data);
    }
  };

  ws.onerror = () => {
    if (disposed || opened) return;
    clearConnectTimeout();
    triggerFallback();
  };

  ws.onclose = () => {
    if (disposed) return;
    clearConnectTimeout();
    if (opened) {
      emit({ ...data, connected: false });
    } else {
      triggerFallback();
    }
  };

  return () => {
    disposed = true;
    clearConnectTimeout();
    if (ws) {
      ws.close();
      ws = null;
    }
  };
}
