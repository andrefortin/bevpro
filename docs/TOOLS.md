# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Gemini API Key: The `GEMINI_API_KEY` environment variable must be set in the environment to enable `web_search` functionality.

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Contact Information (Updated)

- **Mobile Phone:** `+13432622451` (Canadian Cell, Koodo, Ottawa, ON). **(Primary Contact)**

## Email (SMTP + IMAP)

### andre@fortinmedia.net

- **Provider:** Gmail (Google Workspace)
- **SMTP Host:** smtp.gmail.com
- **SMTP Port:** 587 (STARTTLS)
- **IMAP Host:** imap.gmail.com
- **IMAP Port:** 993 (SSL)
- **User:** andre@fortinmedia.net
- **App Password:** `znda pwor owil elfv`
- **From:** andre@fortinmedia.net
- **Verified:** 2026-04-18 ✅ (sent + confirmed via IMAP)

### Outreach Credentials (New)

This section is for storing API keys for outbound services. These must be set as environment variables.

- **Twilio:**
  - SID: `ACxxxxxxxxxxxx`
  - Auth Token: `your-secret-auth-token`
- **General:**
  - Any other API keys needed (e.g., SMS provider API Key).

### How to send (Python)

```python
# ... (rest of the script remains the same)
```

### How to read inbox (Python IMAP)

```python
# ... (script remains the same)
```
