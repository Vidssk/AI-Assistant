import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const frontendRoot = path.resolve(__dirname, "..");
const demoPath = path.resolve(frontendRoot, "../../backend/snapshots/demo.json");
const outputPath = path.resolve(frontendRoot, "public/snapshot.json");

if (!fs.existsSync(demoPath)) {
  console.error(`Demo snapshot not found: ${demoPath}`);
  console.error("Run: cd backend && python refresh_demo_snapshot.py");
  process.exit(1);
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.copyFileSync(demoPath, outputPath);
console.log("Synced demo.json -> public/snapshot.json");
