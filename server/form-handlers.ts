import nodemailer from "nodemailer";

/**
 * Shared form-submission handlers. Delivers lead emails to LEAD_EMAIL
 * (info@mybevpro.com) via the configured Gmail SMTP sender.
 *
 * Env vars (same as email-send skill): SMTP_HOST, SMTP_PORT, SMTP_USER,
 * SMTP_PASS, SMTP_FROM. Set on Vercel (Production) for the live site.
 */

const LEAD_EMAIL = process.env.LEAD_EMAIL ?? "info@mybevpro.com";

type AnyRecord = Record<string, unknown>;

function transport() {
  return nodemailer.createTransport({
    host: process.env.SMTP_HOST || "smtp.gmail.com",
    port: Number(process.env.SMTP_PORT || 587),
    secure: false,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  });
}

async function sendLeadEmail(opts: { subject: string; text: string; replyTo: string }) {
  await transport().sendMail({
    from: process.env.SMTP_FROM || process.env.SMTP_USER,
    to: LEAD_EMAIL,
    replyTo: opts.replyTo,
    subject: opts.subject,
    text: opts.text,
  });
}

function isBot(body: AnyRecord | null | undefined): boolean {
  // Honeypot: real users never see this field, bots fill it blindly.
  return Boolean(body?.website);
}

function fmt(label: string, value: unknown): string | null {
  if (value === undefined || value === null || value === "") return null;
  return `${label}: ${String(value)}`;
}

function lines(rows: Array<string | null>): string {
  return rows.filter((r): r is string => r !== null).join("\n");
}

export interface HandlerResult {
  status: number;
  json: { success: boolean; error?: string };
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const SERVICE_LABELS: Record<string, string> = {
  premium: "Premium Bar Package",
  essential: "Essential Bar Package",
  mixers: "Mixers / Cocktail Stations",
  wine: "Wine Tasting",
  mocktail: "Mocktail Packages",
  coffee: "Coffee Catering",
  multiple: "Multiple Services",
  unsure: "Not Sure Yet",
};

const EVENT_LABELS: Record<string, string> = {
  Wedding: "Wedding",
  Anniversary: "Anniversary",
  Corporate: "Corporate Event",
  Birthday: "Birthday Party",
  Gala: "Gala / Fundraiser",
  Holiday: "Holiday Party",
  Other: "Other",
};

export async function handleIntake(body: unknown): Promise<HandlerResult> {
  const data = (body ?? {}) as AnyRecord;

  if (isBot(data)) return { status: 200, json: { success: true } };

  const fullName = String(data.fullName ?? "").trim();
  const email = String(data.email ?? "").trim();
  if (!fullName || !EMAIL_RE.test(email)) {
    return { status: 400, json: { success: false, error: "Name and a valid email are required." } };
  }

  const text = lines([
    "NEW QUOTE REQUEST — BevPro Intake Form",
    `Submitted: ${new Date().toLocaleString("en-US", { timeZone: "America/Toronto" })}`,
    "",
    "EVENT DETAILS",
    fmt("Type", EVENT_LABELS[String(data.eventType ?? "")] ?? data.eventType),
    fmt("Event name", data.eventName),
    fmt("Date", data.eventDate),
    fmt("Location", data.eventLocation),
    fmt("Start time", data.startTime),
    fmt("End time", data.endTime),
    fmt("Bar service hours", data.barHours),
    fmt("Guests", data.guestCount),
    fmt("Service package", SERVICE_LABELS[String(data.serviceType ?? "")] ?? data.serviceType),
    fmt("Bartenders", data.bartenders),
    fmt("Barbacks", data.barbacks),
    fmt("Glassware rental", data.glasswareRental === "yes" ? "Yes" : data.glasswareRental === "no" ? "No" : data.glasswareRental),
    fmt("Venue bar available", data.venueBar === "yes" ? "Yes" : data.venueBar === "no" ? "No" : data.venueBar),
    fmt("Notes", data.otherNotes),
    "",
    "CONTACT",
    fmt("Name", fullName),
    fmt("Email", email),
    fmt("Phone", data.phone),
    fmt("Referral source", data.referralSource),
    "",
    "Reply to this email to respond directly to the lead.",
  ]);

  try {
    await sendLeadEmail({
      subject: `BevPro Quote Request — ${fullName} (${String(data.eventType ?? "event")})`,
      replyTo: email,
      text,
    });
    return { status: 200, json: { success: true } };
  } catch (err) {
    console.error("[form-handlers] intake email failed:", err);
    return { status: 500, json: { success: false, error: "Could not send your request. Please try again or email us directly." } };
  }
}

export async function handleContact(body: unknown): Promise<HandlerResult> {
  const data = (body ?? {}) as AnyRecord;

  if (isBot(data)) return { status: 200, json: { success: true } };

  const name = String(data.name ?? "").trim();
  const email = String(data.email ?? "").trim();
  if (!name || !EMAIL_RE.test(email)) {
    return { status: 400, json: { success: false, error: "Name and a valid email are required." } };
  }

  const text = lines([
    "NEW INQUIRY — BevPro Contact Form",
    `Submitted: ${new Date().toLocaleString("en-US", { timeZone: "America/Toronto" })}`,
    "",
    "EVENT DETAILS",
    fmt("Date", data.eventDate),
    fmt("Type", data.eventType),
    fmt("Service interest", data.service),
    fmt("Guest count", data.guestCount),
    fmt("Duration (hours)", data.duration),
    fmt("Venue / location", data.location),
    fmt("Notes", data.notes),
    "",
    "CONTACT",
    fmt("Name", name),
    fmt("Company", data.company),
    fmt("Email", email),
    fmt("Phone", data.phone),
    "",
    "Reply to this email to respond directly to the lead.",
  ]);

  try {
    await sendLeadEmail({
      subject: `BevPro Contact Inquiry — ${name}`,
      replyTo: email,
      text,
    });
    return { status: 200, json: { success: true } };
  } catch (err) {
    console.error("[form-handlers] contact email failed:", err);
    return { status: 500, json: { success: false, error: "Could not send your request. Please try again or email us directly." } };
  }
}
