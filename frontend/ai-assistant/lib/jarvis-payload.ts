import type { JarvisData, JarvisPayload } from "./jarvis-types";

export function parsePayload(data: unknown): JarvisPayload | null {
  if (!data || typeof data !== "object") return null;

  const obj = data as Record<string, unknown>;

  if (obj.dashboard && typeof obj.dashboard === "object") {
    return obj.dashboard as JarvisPayload;
  }

  if (obj.status !== undefined) return obj as JarvisPayload;

  if (obj.type === "state" && obj.data && typeof obj.data === "object") {
    return obj.data as JarvisPayload;
  }
  if (obj.type === "event" && obj.data && typeof obj.data === "object") {
    return obj.data as JarvisPayload;
  }

  return null;
}

export function applyPayload(
  payload: JarvisPayload,
  prev: JarvisData
): JarvisData {
  return {
    status: payload.status !== undefined ? payload.status : prev.status,
    agent: payload.agent !== undefined ? payload.agent : prev.agent,
    events: payload.events !== undefined ? payload.events : prev.events,
    system: payload.system !== undefined ? payload.system : prev.system,
    response:
      payload.response !== undefined ? payload.response : prev.response,
    responses:
      payload.responses !== undefined ? payload.responses : prev.responses,
    connected: prev.connected,
    source: prev.source,
    error: prev.error,
  };
}
