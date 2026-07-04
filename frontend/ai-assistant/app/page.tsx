// "use client";

// import { useEffect, useState } from "react";

// export default function Home() {
//   const [status, setStatus] = useState("connecting...");
//   const [agent, setAgent] = useState<string | null>(null);
//   const [connected, setConnected] = useState(false);

//   useEffect(() => {
//     const ws = new WebSocket("ws://127.0.0.1:8000/ws");

//     ws.onopen = () => {
//       console.log("WS OPEN");
//       setConnected(true);
//     };

//     ws.onmessage = (event) => {
//       console.log("WS RAW:", event.data);

//       try {
//         const data = JSON.parse(event.data);
//         const payload =
//           data?.status !== undefined
//             ? data
//             : data?.type === "state" && data?.data
//               ? data.data
//               : data?.type === "event" && data?.data
//                 ? data.data
//                 : null;

//         if (payload?.status !== undefined) {
//           setStatus(payload.status);
//         }

//         if (payload?.agent !== undefined) {
//           setAgent(payload.agent);
//         }
//       } catch (err) {
//         console.error("Failed to parse WS message:", event.data);
//       }
//     };

//     ws.onerror = (err) => {
//       console.error("WS ERROR:", err);
//       setConnected(false);
//     };

//     ws.onclose = () => {
//       console.log("WS CLOSED");
//       setConnected(false);
//     };

//     return () => {
//       ws.close();
//     };
//   }, []);

//   return (
//     <main className="p-8">
//       <h1 className="text-2xl font-bold mb-4">Jarvis Dashboard</h1>

//       <div className="space-y-2">
//         <p>
//           Status: <strong>{status}</strong>
//         </p>

//         <p>
//           Agent: <strong>{agent ?? "None"}</strong>
//         </p>

//         <p>
//           WebSocket:{" "}
//           <span style={{ color: connected ? "green" : "red" }}>
//             {connected ? "connected" : "disconnected"}
//           </span>
//         </p>
//       </div>
//     </main>
//   );
// }
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