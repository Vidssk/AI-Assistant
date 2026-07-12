"use client";

import { useEffect, useState } from "react";
import { subscribeJarvisData } from "@/lib/jarvis-data-source";
import type { JarvisData } from "@/lib/jarvis-types";

const initialState: JarvisData = {
  status: "connecting...",
  agent: null,
  events: [],
  system: null,
  connected: false,
};

export function useJarvisData(): JarvisData {
  const [data, setData] = useState<JarvisData>(initialState);

  useEffect(() => subscribeJarvisData(setData), []);

  return data;
}
