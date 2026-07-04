"use client";

import { FRAME_OUTER_PADDING_CLASS } from "./frameAssets";
// import HudFrame from "./HudFrame"; 
import Hud from "./Hud";
interface FrameProps {
  children: React.ReactNode;
}

export default function Frame({ children }: FrameProps) {
  return (
    <div
      className={`absolute inset-0 overflow-hidden ${FRAME_OUTER_PADDING_CLASS}`}
    >
      {/* Hud */}
      <Hud>
        {children}
      </Hud>
    </div>
  );
}