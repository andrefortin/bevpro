# Mixers Package Email — Theme Swap Guide

Applies to all three HTML templates. Each has `<!-- SWAP:` comments at the swappable spots.

## Template files

| File | Angle | Best for |
|------|-------|----------|
| `byob-mixers-romantic.html` | Emotional / Trust | First-time planners, venue referrals |
| `byob-mixers-numbers.html` | Price / Savings | "Too expensive" objections, comparison shoppers |
| `byob-mixers-insider.html` | Conversational / Personal | BYOB seekers, specific drink requests |

All three share the same swap points below.

---

## Swappable values (search for `<!-- SWAP:` comments in each HTML)

| # | What | Wedding (default) | Birthday | Corporate |
|---|------|-------------------|----------|-----------|
| 1 | **Hero image** | `photo-1511795409834-ef04bbd61622` (wedding toast) | `photo-1530103862676-de8c9debad1d` (private party) | `photo-1540575467063-178a50c2df87` (corporate) |
| 2 | **Badge label** | `Wedding Package` | `Birthday Package` | `Corporate Package` |
| 3 | **Subject line** | "Leave your wedding bar to the Pros 🍸" | "Your birthday bar, minus the markup 🎂" | "Your corporate bar, minus the 300% markup" |
| 4 | **Drink references** (insider only) | espresso martinis, old fashioneds, margaritas | margaritas, mojitos, Aperol spritzes | classic cocktails, wine, craft beer |
| 5 | **Savings example** | `A typical 150-guest wedding` | `A typical 80-guest birthday` | `A typical 200-guest corporate event` |
| 6 | **CTA text** | `Get Your Custom Proposal` | `Get Your Party Quote` | `Get Your Event Quote` |

## Image library (all Unsplash, all verified)

```
Wedding toast:     photo-1511795409834-ef04bbd61622
Bartender at event: photo-1514362545857-3bc16c4c7d1b
Cocktail detail:   photo-1544148103-0773bf10d330
Private party:     photo-1530103862676-de8c9debad1d
Corporate event:   photo-1540575467063-178a50c2df87
Team activity:     photo-1528605248644-14dd04022da1
```

All images require `ixlib=rb-4.0.3`. Hero images use `w=1200`.

## Sending the email

1. Pick the template that matches the prospect (see EMAIL-CAMPAIGN-VERSIONS.md for decision guide)
2. Replace `{{first_name}}` and `{{unsubscribe_url}}`
3. Swap theme values per the table above if needed
4. Test rendering (Litmus, Email on Acid, or send to yourself first)
5. Send via SMTP provider

## Form link

All templates point to `https://mybevpro.com/intake` — the event planning intake form.
