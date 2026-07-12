export type JarvisEvent = { timestamp: string; event: string };

export type JarvisResponse = {
  timestamp: string;
  agent: string | null;
  response: string;
};

export type JarvisPayload = {
  status: string;
  agent: string | null;
  events?: JarvisEvent[];
  system?: SystemInfo | null;
  response?: JarvisResponse | null;
};

export interface CpuInfo {
  usage: number;
  temperature: number;
}

export interface GpuInfo {
  name: string;
  usage: number;
  temperature: number;
  vram_used: number;
  vram_total: number;
}

export interface MemoryInfo {
  used: number;
  total: number;
}

export interface SystemInfo {
  cpu: CpuInfo;
  gpu: GpuInfo;
  memory: MemoryInfo;
}

export type JarvisSource = "connecting" | "live" | "snapshot";

export type JarvisData = {
  status: string;
  agent: string | null;
  events: JarvisEvent[];
  system: SystemInfo | null;
  response: JarvisResponse | null;
  connected: boolean;
  source: JarvisSource;
  error: string | null;
};
