import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";

/**
 * Cost Tracker Extension (bevpro)
 *
 * Tracks LLM token costs per session. Appends a session-cost line to the
 * project cost log on session end. Reads pipeline ledger (~/.forge-writer/cost_ledger.jsonl)
 * when present for pipeline-side costs.
 *
 * Ledger format: one JSON object per line
 *   { "ts": "...", "project": "bevpro", "model": "...", "prompt_tokens": N, "completion_tokens": N, "cost_usd": 0.00 }
 */
export default function (pi: ExtensionAPI) {
  const LEDGER = path.join(os.homedir(), ".forge-writer", "cost_ledger.jsonl");
  const COST_LOG = path.join(os.homedir(), "batcave", "bevpro", ".pi", "cost-log.jsonl");

  function appendCost(entry: Record<string, unknown>) {
    try {
      fs.appendFileSync(COST_LOG, JSON.stringify(entry) + "\n");
    } catch (e) {
      console.error("[cost-tracker] append failed:", e);
    }
  }

  pi.on("session_end", async (event: any, ctx: any) => {
    const usage = event?.usage || ctx?.usage || {};
    const model = event?.model || ctx?.model || "unknown";
    const entry = {
      ts: new Date().toISOString(),
      project: "bevpro",
      model,
      prompt_tokens: usage.prompt_tokens ?? 0,
      completion_tokens: usage.completion_tokens ?? 0,
      total_tokens: (usage.prompt_tokens ?? 0) + (usage.completion_tokens ?? 0),
      source: "pi-session",
    };
    appendCost(entry);

    // Pipeline-side costs (if ledger exists) — summarize bevpro entries
    if (fs.existsSync(LEDGER)) {
      try {
        const lines = fs.readFileSync(LEDGER, "utf8").split("\n").filter(Boolean);
        const bevpro = lines
          .map((l) => { try { return JSON.parse(l); } catch { return null; } })
          .filter((e) => e && e.project === "bevpro");
        if (bevpro.length) {
          const total = bevpro.reduce((s, e) => s + (e.cost_usd || 0), 0);
          ctx.ui.notify(`💰 bevpro pipeline ledger: ${bevpro.length} calls, $${total.toFixed(4)}`, "info");
        }
      } catch { /* ledger unreadable — ignore */ }
    }
  });
}
