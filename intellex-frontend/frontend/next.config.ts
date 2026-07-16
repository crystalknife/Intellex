import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Bundles a minimal, self-contained server (only the node_modules
  // actually used, traced automatically) into .next/standalone --
  // without this, the Docker runtime image would need the full
  // node_modules tree copied in, which is dramatically larger.
  output: "standalone",
};

export default nextConfig;
