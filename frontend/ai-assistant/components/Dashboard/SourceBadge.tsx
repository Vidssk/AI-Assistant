import type { JarvisSource } from "@/lib/jarvis-types";

const SOURCE_CONFIG: Record<
  JarvisSource,
  { label: string; dotClass: string; textClass: string }
> = {
  live: {
    label: "LIVE BACKEND",
    dotClass: "bg-green-400 animate-pulse",
    textClass: "text-green-400/90",
  },
  snapshot: {
    label: "DEMO SNAPSHOT",
    dotClass: "bg-amber-400",
    textClass: "text-amber-400/90",
  },
  connecting: {
    label: "CONNECTING",
    dotClass: "bg-cyan-400 animate-pulse",
    textClass: "text-cyan-400/90",
  },
};

interface SourceBadgeProps {
  source: JarvisSource;
}

export default function SourceBadge({ source }: SourceBadgeProps) {
  const config = SOURCE_CONFIG[source];

  return (
    <div
      className="flex items-center gap-2 px-3 py-1 border border-cyan-500/30 rounded bg-black/40 backdrop-blur-sm"
      role="status"
      aria-live="polite"
    >
      <span className={`h-1.5 w-1.5 rounded-full ${config.dotClass}`} />
      <span
        className={`font-mono text-[10px] tracking-widest uppercase ${config.textClass}`}
      >
        {config.label}
      </span>
    </div>
  );
}

export function connectionLabel(source: JarvisSource): {
  text: string;
  className: string;
} {
  switch (source) {
    case "live":
      return { text: "live backend", className: "text-green-400" };
    case "snapshot":
      return { text: "demo snapshot", className: "text-amber-400" };
    case "connecting":
      return { text: "connecting...", className: "text-cyan-400" };
  }
}
