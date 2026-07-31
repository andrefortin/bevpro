import type { IncomingMessage, ServerResponse } from "node:http";
import { handleContact } from "../server/form-handlers";

export default async function handler(req: IncomingMessage, res: ServerResponse) {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({ success: false, error: "Method not allowed" }));
    return;
  }

  const result = await handleContact((req as { body?: unknown }).body);
  res.statusCode = result.status;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(result.json));
}
