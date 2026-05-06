#!/usr/bin/env python3
"""
outreach-launcher-local — Sends a single outreach touch (email or SMS).

This skill is stateless — it sends and reports. All DB writes happen in the caller.

Usage:
  python3 outreach-launcher.py <event_json_path> [--output <path>]

Input JSON:
  {
    "channel":    "email" | "sms",
    "to":         "recipient@example.com" | "+15551234567",
    "subject":    "...",              (email only)
    "body":       "...",
    "from_email": "andre@...",        (email only)
    "smtp_host":  "smtp.gmail.com",   (email only)
    "smtp_port":  587,                (email only)
    "smtp_user":  "...",              (email only)
    "smtp_pass":  "...",              (email only)
    "twilio_sid": "...",              (sms only, optional)
    "twilio_token": "...",            (sms only, optional)
    "twilio_from":  "+1...",          (sms only, optional)
    "test": false                     (routes to from_email with [TEST] prefix)
  }

Output JSON:
  { "success": true, "to": "...", "channel": "email" }
  { "success": false, "error": "..." }
"""

import sys
import json
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(cfg: dict) -> dict:
    to = cfg["to"]
    subject = cfg.get("subject", "")
    body = cfg.get("body", "")
    from_email = cfg.get("from_email") or cfg.get("smtp_user")

    if cfg.get("test"):
        to = from_email
        subject = f"[TEST] {subject}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(cfg["smtp_host"], int(cfg["smtp_port"])) as s:
            s.ehlo()
            s.starttls()
            s.login(cfg["smtp_user"], cfg["smtp_pass"])
            s.sendmail(from_email, [to], msg.as_string())
        return {"success": True, "to": to, "channel": "email"}
    except Exception as e:
        return {"success": False, "error": str(e), "channel": "email"}


def send_sms(cfg: dict) -> dict:
    sid = cfg.get("twilio_sid")
    token = cfg.get("twilio_token")
    from_num = cfg.get("twilio_from")
    to = cfg.get("to")
    body = cfg.get("body", "")

    if cfg.get("test"):
        return {"success": True, "to": to, "channel": "sms", "test": True,
                "note": "SMS test mode: not actually sent"}

    if not all([sid, token, from_num, to]):
        return {"success": False, "error": "Twilio credentials or recipient missing", "channel": "sms"}

    try:
        from twilio.rest import Client
        client = Client(sid, token)
        message = client.messages.create(body=body, from_=from_num, to=to)
        return {"success": True, "to": to, "channel": "sms", "sid": message.sid}
    except ImportError:
        return {"success": False, "error": "twilio package not installed (pip install twilio)", "channel": "sms"}
    except Exception as e:
        return {"success": False, "error": str(e), "channel": "sms"}


def launch(cfg: dict) -> dict:
    channel = cfg.get("channel", "email")
    if channel == "email":
        return send_email(cfg)
    elif channel == "sms":
        return send_sms(cfg)
    else:
        return {"success": False, "error": f"Unknown channel: {channel}"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("event_json", help="Path to event config JSON")
    parser.add_argument("--output", help="Output path (default: stdout)")
    args = parser.parse_args()

    with open(args.event_json) as f:
        cfg = json.load(f)

    result = launch(cfg)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
