import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

/**
 * Model Fallback Extension (bevpro)
 *
 * Falls back to alternative providers when DeepSeek is down:
 *   deepseek-v4-pro   → anthropic/claude-sonnet-4-20250514
 *   deepseek-v4-flash → google/gemini-2.5-flash-001
 */
export default function (pi: ExtensionAPI) {
  const FALLBACKS: Record<string, string> = {
    "deepseek/deepseek-v4-pro": "anthropic/claude-sonnet-4-20250514",
    "deepseek/deepseek-v4-flash": "google/gemini-2.5-flash-001",
  };

  pi.on("model_error", async (event: any, ctx: any) => {
    const failedModel = event.model || "";
    const fallback = FALLBACKS[failedModel];

    if (fallback) {
      ctx.ui.notify(`⚠️ ${failedModel} failed, falling back to ${fallback}`, "warning");
      return { retryWithModel: fallback };
    }

    ctx.ui.notify(`❌ Model ${failedModel} failed, no fallback configured`, "error");
    return null;
  });
}
