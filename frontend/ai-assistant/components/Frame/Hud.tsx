import "./Hud.css";
import { ReactNode } from "react";

interface HudProps {
  children?: ReactNode;
}

export default function Hud({ children }: HudProps) {
  return (
    <div className="hud">
      <div className="hud-grid">
        <div className="tl"></div>
        <div className="top"></div>
        <div className="tr"></div>

        <div className="left"></div>
        <div className="center"></div>
        <div className="right"></div>

        <div className="bl"></div>
        <div className="bottom"></div>
        <div className="br"></div>
      </div>

      <div className="hud-content">
        {children}
      </div>
    </div>
  );
}