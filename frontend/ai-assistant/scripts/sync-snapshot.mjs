import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const frontendRoot = path.resolve(__dirname, "..");
const snapshotsDir = path.resolve(frontendRoot, "../../backend/snapshots");
const outputPath = path.resolve(frontendRoot, "public/snapshot.json");

function findLatestSnapshot() {
  if (!fs.existsSync(snapshotsDir)) {
    console.warn(`Snapshots directory not found: ${snapshotsDir}`);
    return null;
  }

  const snapshotFiles = fs
    .readdirSync(snapshotsDir)
    .filter((name) => name.startsWith("snapshot-") && name.endsWith(".json"))
    .map((name) => {
      const fullPath = path.join(snapshotsDir, name);
      return { name, fullPath, mtime: fs.statSync(fullPath).mtime };
    })
    .sort((a, b) => b.mtime - a.mtime);

  if (snapshotFiles.length > 0) {
    return snapshotFiles[0];
  }

  const demoPath = path.join(snapshotsDir, "demo.json");
  if (fs.existsSync(demoPath)) {
    console.warn("No snapshot-*.json found; falling back to demo.json");
    return { name: "demo.json", fullPath: demoPath, mtime: fs.statSync(demoPath).mtime };
  }

  return null;
}

const latest = findLatestSnapshot();

if (!latest) {
  console.error("No snapshot files found to sync.");
  process.exit(1);
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.copyFileSync(latest.fullPath, outputPath);
console.log(`Synced ${latest.name} -> public/snapshot.json`);
