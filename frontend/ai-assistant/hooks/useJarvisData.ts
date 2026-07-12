"use client";

import { useEffect, useState } from "react";
import { initialData, subscribeJarvisData } from "@/lib/jarvis-data-source";
import type { JarvisData } from "@/lib/jarvis-types";

export function useJarvisData(): JarvisData {
  const [data, setData] = useState<JarvisData>(initialData);

  useEffect(() => subscribeJarvisData(setData), []);

  return data;
}
