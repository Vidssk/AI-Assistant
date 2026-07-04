import React from "react";
import Frame from "../Frame/Frame";
import { HudItem } from "../Frame/HudItem";

function Dashboard() {
  return (
    <div className="w-full h-full min-h-0 p-4 grid grid-cols-2 grid-rows-[minmax(0,1fr)_11rem] gap-4">
      {/* Top left */}
      <div className="min-h-0 min-w-0">
        <Frame>
          <HudItem top={12} left={12}>
            <h2 className="text-white">Main HUD</h2>
          </HudItem>
        </Frame>
      </div>

      {/* Top right */}
      <div className="min-h-0 min-w-0">
        <Frame>
          <HudItem top={12} right={12}>
            <h2 className="text-white">Mini Map</h2>
          </HudItem>
        </Frame>
      </div>

      {/* Bottom — stretched full width */}
      <div className="col-span-2 min-h-0">
        <Frame>
          <HudItem top={12} left={12}>
            <h2 className="text-white">Stats Panel</h2>
          </HudItem>
        </Frame>
      </div>
    </div>
  );
}

export default Dashboard;
