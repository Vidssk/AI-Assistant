"use client";

import type { ReactNode } from "react";
import { useJarvisData } from "@/hooks/useJarvisData";
import { fmtMetric, fmtPair, fmtText } from "@/lib/format";
import Frame from "../Frame/Frame";
import { HudItem } from "../Frame/HudItem";
import SourceBadge from "./SourceBadge";

const AI_NAME = "AI-Mark I";

function pct(used?: number | null, total?: number | null): number | null {
  if (used == null || total == null || total === 0) return null;
  return Math.min(100, Math.max(0, (used / total) * 100));
}

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

function PanelContent({
  title,
  headerRight,
  bodyClassName,
  children,
}: {
  title: string;
  headerRight?: ReactNode;
  bodyClassName?: string;
  children: ReactNode;
}) {
  return (
    <HudItem top={12} left={12} right={12} bottom={12}>
      <div className="flex flex-col h-full min-h-0">
        <div className="flex items-center justify-between gap-2 mb-3 shrink-0">
          <h2 className="text-cyan-300 text-sm font-semibold tracking-wide">
            {title}
          </h2>
          {headerRight}
        </div>
        <div
          className={[
            "flex-1 min-h-0 overflow-y-auto",
            bodyClassName,
          ]
            .filter(Boolean)
            .join(" ")}
        >
          {children}
        </div>
      </div>
    </HudItem>
  );
}

const METRIC_BLOCK_W = "10.5rem";

function MetricBar({
  label,
  value,
  percent,
  trailing,
}: {
  label: string;
  value: string;
  percent?: number | null;
  trailing?: ReactNode;
}) {
  const fill = percent ?? 0;

  return (
    <div className="space-y-1 shrink-0" style={{ width: METRIC_BLOCK_W }}>
      <div className="grid grid-cols-[auto_1fr] gap-x-2 items-center text-xs">
        <span className="text-cyan-400/70 shrink-0">{label}</span>
        <div className="flex items-center justify-end gap-2 min-w-0">
          {trailing}
          <span className="text-cyan-300 tabular-nums truncate">{value}</span>
        </div>
      </div>
      <div className="h-1.5 w-full rounded-full bg-cyan-500/10 overflow-hidden">
        <div
          className="h-full rounded-full bg-cyan-400/60 transition-all duration-500"
          style={{ width: percent == null ? "0%" : `${fill}%` }}
        />
      </div>
    </div>
  );
}

function SectionLabel({ children }: { children: ReactNode }) {
  return (
    <p className="text-cyan-400/70 text-[10px] uppercase tracking-widest pt-3 mt-3 border-t border-cyan-500/15 first:mt-0 first:pt-0 first:border-t-0">
      {children}
    </p>
  );
}

function StatusDot({ active = false }: { active?: boolean }) {
  return (
    <span
      className={[
        "inline-block h-1.5 w-1.5 rounded-full shrink-0",
        active ? "bg-green-400 animate-pulse" : "bg-cyan-400/60",
      ].join(" ")}
    />
  );
}

export default function Dashboard() {
  const { status, agent, events, system, source, error } = useJarvisData();
  const isConnecting = source === "connecting";
  const showErrorBanner =
    error !== null && events.length === 0 && system === null && !isConnecting;
  const isActive = status.toLowerCase() === "active";

  const vramPercent = pct(system?.gpu?.vram_used, system?.gpu?.vram_total);
  const memoryPercent = pct(system?.memory?.used, system?.memory?.total);

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
          <PanelContent
            title="AI Information"
            headerRight={<SourceBadge source={source} />}
          >
            {isConnecting ? (
              <LoadingPlaceholder lines={4} />
            ) : (
              <div className="space-y-1 text-sm">
                <div className="grid grid-cols-[auto_1fr] gap-x-3 gap-y-2 pb-1">
                  <span className="text-cyan-400/70">Name</span>
                  <span className="text-cyan-300">{AI_NAME}</span>
                  <span className="text-cyan-400/70">Status</span>
                  <span className="flex items-center gap-2 text-cyan-300">
                    <StatusDot active={isActive} />
                    {status}
                  </span>
                </div>

                <SectionLabel>GPU</SectionLabel>
                <p className="text-cyan-300 text-xs truncate mb-2">
                  {fmtText(system?.gpu?.name)}
                </p>
                <div className="space-y-2.5">
                  <MetricBar
                    label="Usage"
                    value={fmtMetric(system?.gpu?.usage, "%")}
                    percent={system?.gpu?.usage}
                    trailing={
                      system?.gpu?.temperature != null ? (
                        <span className="px-1.5 py-0.5 rounded border border-cyan-500/25 bg-cyan-500/5 text-cyan-400/80 text-[10px] tabular-nums">
                          {fmtMetric(system?.gpu?.temperature, "°C")}
                        </span>
                      ) : null
                    }
                  />
                  <MetricBar
                    label="VRAM"
                    value={fmtPair(
                      system?.gpu?.vram_used,
                      system?.gpu?.vram_total,
                      " GB"
                    )}
                    percent={vramPercent}
                  />
                </div>

                <SectionLabel>CPU</SectionLabel>
                <MetricBar
                  label="Usage"
                  value={fmtMetric(system?.cpu?.usage, "%")}
                  percent={system?.cpu?.usage}
                />

                <SectionLabel>Memory</SectionLabel>
                <MetricBar
                  label="Usage"
                  value={fmtPair(
                    system?.memory?.used,
                    system?.memory?.total,
                    " GB"
                  )}
                  percent={memoryPercent}
                />
              </div>
            )}
          </PanelContent>
        </Frame>
      </div>

      {/* Col 2 — Agents */}
      <div className="min-h-0 min-w-0">
        <Frame>
          <PanelContent title="Agents">
            {isConnecting ? (
              <LoadingPlaceholder lines={2} />
            ) : agent ? (
              <div className="rounded border border-cyan-500/25 bg-cyan-500/5 p-3 space-y-2">
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 min-w-0">
                    <span className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse shrink-0" />
                    <span className="text-cyan-300 font-medium truncate">
                      {agent}
                    </span>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 border border-cyan-500/40 text-cyan-400 rounded uppercase tracking-wider shrink-0">
                    {status}
                  </span>
                </div>
                <p className="text-cyan-400/50 text-xs pl-4">
                  Task in progress
                </p>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-full min-h-[6rem] text-center px-4">
                <span className="h-3 w-3 rounded-full border border-cyan-500/30 mb-3" />
                <p className="text-cyan-400/60 text-sm">No agents running</p>
                <p className="text-cyan-400/30 text-xs mt-1">
                  Agents will appear here when active
                </p>
              </div>
            )}
          </PanelContent>
        </Frame>
      </div>

      {/* Col 3 — Review */}
      <div className="min-h-0 min-w-0">
        <Frame>
          <PanelContent title="Review" bodyClassName="flex flex-col">
            {isConnecting ? (
              <LoadingPlaceholder lines={2} />
            ) : (
              <div className="flex flex-col flex-1 min-h-0">
                <p className="text-cyan-400/50 text-[10px] uppercase tracking-widest mb-2 shrink-0">
                  Output
                </p>
                <div className="flex-1 min-h-[10rem] rounded border border-dashed border-cyan-500/20 bg-black/30 font-mono text-sm flex items-center justify-center p-4">
                  <div className="text-center">
                    <p className="text-cyan-200/80">
                      No results pending review
                    </p>
                    <p className="text-cyan-400/40 text-xs mt-2">
                      Approval workflow coming soon
                    </p>
                  </div>
                </div>
              </div>
            )}
          </PanelContent>
        </Frame>
      </div>

      {/* Bottom — History Log */}
      <div className="min-h-0 lg:col-span-3">
        <Frame>
          <PanelContent title="History Log">
            {isConnecting ? (
              <LoadingPlaceholder lines={5} />
            ) : events.length > 0 ? (
              <ul className="divide-y divide-cyan-500/10 font-mono text-xs">
                {events.map((entry, i) => (
                  <li
                    key={`${entry.timestamp}-${i}`}
                    className="flex gap-3 py-2 px-1 hover:bg-cyan-500/5 transition-colors"
                  >
                    <span className="text-cyan-400/50 shrink-0 w-[7.5rem] tabular-nums">
                      {entry.timestamp}
                    </span>
                    <span className="text-cyan-200/80 min-w-0 break-words">
                      {entry.event}
                    </span>
                  </li>
                ))}
              </ul>
            ) : showErrorBanner ? (
              <p className="text-amber-400/70 text-sm font-mono">{error}</p>
            ) : (
              <p className="text-cyan-400/50 text-sm">Waiting for events...</p>
            )}
          </PanelContent>
        </Frame>
      </div>
    </div>
  );
}
