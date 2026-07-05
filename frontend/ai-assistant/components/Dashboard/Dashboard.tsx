"use client";

import { useEffect, useState } from "react";
import Frame from "../Frame/Frame";
import { HudItem } from "../Frame/HudItem";

const AI_NAME = "AI-Mark I";

type JarvisEvent = { timestamp: string; event: string };
type JarvisPayload = {
  status: string;
  agent: string | null;
  events?: JarvisEvent[];
};

function parsePayload(data: unknown): JarvisPayload | null {
  if (!data || typeof data !== "object") return null;

  const obj = data as Record<string, unknown>;
  if (obj.status !== undefined) return obj as JarvisPayload;

  if (obj.type === "state" && obj.data && typeof obj.data === "object") {
    return obj.data as JarvisPayload;
  }
  if (obj.type === "event" && obj.data && typeof obj.data === "object") {
    return obj.data as JarvisPayload;
  }

  return null;
}

export default function Dashboard() {
  const [status, setStatus] = useState("connecting...");
  const [agent, setAgent] = useState<string | null>(null);
  const [events, setEvents] = useState<JarvisEvent[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onopen = () => {
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const payload = parsePayload(data);
        if (!payload) return;

        if (payload.status !== undefined) setStatus(payload.status);
        if (payload.agent !== undefined) setAgent(payload.agent);
        if (payload.events !== undefined) setEvents(payload.events);
      } catch {
        console.error("Failed to parse WS message:", event.data);
      }
    };

    ws.onerror = () => {
      setConnected(false);
    };

    ws.onclose = () => {
      setConnected(false);
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="w-full h-full min-h-0 p-4 grid grid-cols-[1fr_1fr_2fr] grid-rows-[minmax(0,1fr)_minmax(11rem,38%)] gap-4">
      {/* Col 1 — AI Information */}
      <div className="min-h-0 min-w-0">
        <Frame>
          <HudItem top={12} left={12} right={12} bottom={12}>
            <h2 className="text-cyan-300 text-sm font-semibold tracking-wide mb-3">
              AI Information
            </h2>
            <div className="space-y-2 text-cyan-200 text-sm">
              <p>
                <span className="text-cyan-400/70">Name:</span>{" "}
                <span className="text-cyan-300">{AI_NAME}</span>
              </p>
              <p>
                <span className="text-cyan-400/70">Status:</span>{" "}
                <span className="text-cyan-300">{status}</span>
              </p>
              <p>
                <span className="text-cyan-400/70">Connection:</span>{" "}
                <span
                  className={connected ? "text-green-400" : "text-red-400"}
                >
                  {connected ? "connected" : "disconnected"}
                </span>
              </p>
              <p>
                <span className="text-cyan-400/70">CPU:</span> —
              </p>
              <p>
                <span className="text-cyan-400/70">GPU:</span> —
              </p>
            </div>
          </HudItem>
        </Frame>
      </div>

      {/* Col 2 — Agents */}
      <div className="min-h-0 min-w-0">
        <Frame>
          <HudItem top={12} left={12} right={12} bottom={12}>
            <h2 className="text-cyan-300 text-sm font-semibold tracking-wide mb-3">
              Agents
            </h2>
            <div className="space-y-2 text-sm">
              {agent ? (
                <div className="flex items-center justify-between text-cyan-200">
                  <span className="text-cyan-300">{agent}</span>
                  <span className="text-xs px-2 py-0.5 border border-cyan-500/40 text-cyan-400 rounded">
                    {status}
                  </span>
                </div>
              ) : (
                <p className="text-cyan-400/50">No agents running</p>
              )}
              <p className="text-cyan-400/30">—</p>
              <p className="text-cyan-400/30">—</p>
            </div>
          </HudItem>
        </Frame>
      </div>

      {/* Col 3 — Review */}
      <div className="min-h-0 min-w-0">
        <Frame>
          <HudItem top={12} left={12} right={12} bottom={12}>
            <h2 className="text-cyan-300 text-sm font-semibold tracking-wide mb-3">
              Review
            </h2>
            <div className="text-sm">
              <p className="text-cyan-200">No results pending review</p>
              <p className="text-cyan-400/50 mt-2">
                Approval workflow coming soon
              </p>
            </div>
          </HudItem>
        </Frame>
      </div>

      {/* Bottom — History Log */}
      <div className="col-span-3 min-h-0">
        <Frame>
          <HudItem top={12} left={12} right={12} bottom={12}>
            <div className="h-full overflow-y-auto">
              <h2 className="text-cyan-300 text-sm font-semibold tracking-wide mb-3">
                History Log
              </h2>
              {events.length > 0 ? (
                <ul className="space-y-1 font-mono text-xs text-cyan-200/80">
                  {events.map((entry, i) => (
                    <li key={`${entry.timestamp}-${i}`}>
                      <span className="text-cyan-400/60">
                        [{entry.timestamp}]
                      </span>{" "}
                      {entry.event}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-cyan-400/50 text-sm">Waiting for events...</p>
              )}
            </div>
          </HudItem>
        </Frame>
      </div>
    </div>
  );
}
