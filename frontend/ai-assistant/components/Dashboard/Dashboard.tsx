"use client";

import { useJarvisData } from "@/hooks/useJarvisData";
import { fmtMetric, fmtPair, fmtText } from "@/lib/format";
import Frame from "../Frame/Frame";
import { HudItem } from "../Frame/HudItem";
import SourceBadge from "./SourceBadge";

const AI_NAME = "AI-Mark I";

function LoadingPlaceholder({ lines = 3 }: { lines?: number }) {
  return (
    <div className="space-y-2 animate-pulse">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="h-3 rounded bg-cyan-500/10"
          style={{ width: `${70 - i * 12}%` }}
        />
      ))}
      <p className="text-cyan-400/40 text-xs tracking-widest uppercase pt-1">
        Establishing link...
      </p>
    </div>
  );
}

export default function Dashboard() {
  const { status, agent, events, system, source, error } = useJarvisData();
  const isConnecting = source === "connecting";
  const showErrorBanner =
    error !== null && events.length === 0 && system === null && !isConnecting;

  return (
    <div className="relative w-full h-full min-h-0 p-4 overflow-y-auto grid grid-cols-1 auto-rows-[minmax(16rem,auto)] gap-4 lg:overflow-y-hidden lg:grid-cols-[1fr_1fr_2fr] lg:grid-rows-[minmax(0,1fr)_minmax(11rem,38%)] lg:auto-rows-auto">

      {showErrorBanner && (
        <div className="absolute top-2 left-2 right-2 z-10 px-3 py-1.5 border border-amber-500/30 rounded bg-black/50 text-amber-400/90 text-xs font-mono tracking-wide">
          {error}
        </div>
      )}

      {/* Col 1 — AI Information */}
      <div className="min-h-0 min-w-0">
        <Frame>
          <HudItem top={12} left={12} right={12} bottom={12}>
            <h2 className="text-cyan-300 text-sm font-semibold tracking-wide mb-3">
              AI Information
            </h2>
            <p className="flex items-center gap-2 mb-3">
              <span className="text-cyan-400/70 text-sm">Connection:</span>
              <SourceBadge source={source} />
            </p>
            {isConnecting ? (
              <LoadingPlaceholder lines={4} />
            ) : (
              <div className="space-y-2 text-cyan-200 text-sm">
                <p>
                  <span className="text-cyan-400/70">Name:</span>{" "}
                  <span className="text-cyan-300">{AI_NAME}</span>
                </p>
                <p>
                  <span className="text-cyan-400/70">Status:</span>{" "}
                  <span className="text-cyan-300">{status}</span>
                </p>
                <div>
                  <p className="text-cyan-400/70 text-xs uppercase tracking-wide mb-1">
                    GPU
                  </p>
                  <p className="text-cyan-300">{fmtText(system?.gpu?.name)}</p>
                  <p>
                    <span className="text-cyan-400/70">
                      Usage: {fmtMetric(system?.gpu?.usage, "%")}
                    </span>
                  </p>
                  <p>
                    <span className="text-cyan-400/70">
                      Temperature: {fmtMetric(system?.gpu?.temperature, "°C")}
                    </span>
                  </p>
                  <p>
                    <span className="text-cyan-400/70">
                      VRAM: {fmtPair(system?.gpu?.vram_used, system?.gpu?.vram_total, " GB")}
                    </span>
                  </p>
                </div>
                <div>
                  <p className="text-cyan-400/70 text-xs uppercase tracking-wide mb-1">
                    CPU
                  </p>
                  <p>
                    <span className="text-cyan-400/70">
                      Usage: {fmtMetric(system?.cpu?.usage, "%")}
                    </span>
                  </p>
                </div>
                <div>
                  <p className="text-cyan-400/70 text-xs uppercase tracking-wide mb-1">
                    Memory
                  </p>
                  <p>
                    <span className="text-cyan-400/70">
                      Usage: {fmtPair(system?.memory?.used, system?.memory?.total, " GB")}
                    </span>
                  </p>
                </div>
              </div>
            )}
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
            {isConnecting ? (
              <LoadingPlaceholder lines={2} />
            ) : (
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
            )}
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
            {isConnecting ? (
              <LoadingPlaceholder lines={2} />
            ) : (
              <div className="text-sm">
                <p className="text-cyan-200">No results pending review</p>
                <p className="text-cyan-400/50 mt-2">
                  Approval workflow coming soon
                </p>
              </div>
            )}
          </HudItem>
        </Frame>
      </div>

      {/* Bottom — History Log */}
      <div className="min-h-0 lg:col-span-3">
        <Frame>
          <HudItem top={12} left={12} right={12} bottom={12}>
            <h2 className="text-cyan-300 text-sm font-semibold tracking-wide mb-3">
              History Log
            </h2>
            <div className="h-full overflow-y-auto">
              {isConnecting ? (
                <LoadingPlaceholder lines={5} />
              ) : events.length > 0 ? (
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
              ) : showErrorBanner ? (
                <p className="text-amber-400/70 text-sm font-mono">
                  {error}
                </p>
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
