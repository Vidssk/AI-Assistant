"use client";

import Hud from "./Hud";

interface FrameProps {
  children: React.ReactNode;
  width?: string | number;
  height?: string | number;
  className?: string;
}

export default function Frame({
  children,
  width,
  height,
  className,
}: FrameProps) {
  const hasExplicitSize = width != null || height != null;

  return (
    <div
      className={[
        "relative overflow-hidden",
        !hasExplicitSize && "w-full h-full",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
      style={hasExplicitSize ? { width, height } : undefined}
    >
      <Hud>{children}</Hud>
    </div>
  );
}
