# Mixers Package Email — Theme Swap Guide

Use `byob-mixers-wedding.html` as the master template. Swap these 6 values for other themes.

## Places to swap (search for `<!-- SWAP:` comments in the HTML)

| # | What | Wedding (default) | Birthday | Corporate |
|---|------|-------------------|----------|-----------|
| 1 | **Hero image** | `photo-1511795409834-ef04bbd61622` (wedding toast) | `photo-1530103862676-de8c9debad1d` (private party) | `photo-1540575467063-178a50c2df87` (corporate event) |
| 2 | **Badge label** | `Wedding Package` | `Birthday Package` | `Corporate Package` |
| 3 | **Pitch paragraph** | "Planning a wedding..." | "Planning a birthday..." | "Planning a corporate event..." |
| 4 | **Why section heading** | `Your wedding, your alcohol, your budget.` | `Your party, your alcohol, your budget.` | `Your event, your alcohol, your budget.` |
| 5 | **Savings example label** | `A typical 150-guest wedding` | `A typical 80-guest birthday` | `A typical 200-guest corporate event` |
| 6 | **CTA link text** | `Get Your Mixers Quote` | `Get Your Party Quote` | `Get Your Event Quote` |

## Image library (all Unsplash, all verified working)

```
Wedding toast:     photo-1511795409834-ef04bbd61622
Private party:     photo-1530103862676-de8c9debad1d
Corporate event:   photo-1540575467063-178a50c2df87
Team activity:     photo-1528605248644-14dd04022da1
Cocktail detail:   photo-1544148103-0773bf10d330
```

All images use `ixlib=rb-4.0.3` — never remove this or Unsplash returns 404.
For hero headers always use `w=1200` for sharp rendering.

## Sending the email

1. Replace `{{first_name}}` with the recipient's name
2. Replace `{{unsubscribe_url}}` with your unsubscribe link
3. Test with Litmus or Email on Acid for inbox rendering
4. Send via your SMTP provider

## Form link

Points to `https://mybevpro.com/intake` — the full event planning intake form (15 questions, 3 sections).
