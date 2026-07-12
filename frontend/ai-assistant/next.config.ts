import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  turbopack: {
    // Pin project root so Turbopack does not walk up to C:\Users\Santiago\package.json
    root: path.resolve(__dirname),
  },
};

export default nextConfig;
