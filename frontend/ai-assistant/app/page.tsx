"use client";

import { useState } from "react";
import BootScreen from "@/components/BootScreen/BootScreen";
import Dashboard from "@/components/Dashboard/Dashboard";
import Frame from "@/components/Frame/Frame";
import { HudItem } from "@/components/Frame/HudItem";
// import ThreeBackground from "@/components/ThreeBackground/";

export default function Home() {
  const [activated, setActivated] = useState(false);

  return (
    <main className="relative h-screen w-screen overflow-hidden">
      {/* <ThreeBackground /> */}
      <Frame>
        <HudItem top="0%" left="0%" right="0%" bottom="0%">
          {!activated ? (
            <BootScreen onActivate={() => setActivated(true)} />
          ) : (
            <Dashboard />
          )}
        </HudItem>
      </Frame>
    </main>
  );
}
