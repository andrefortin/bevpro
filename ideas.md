# BevPro Website Design

## Design: **Wolfgang Puck Inspired — Green & Gold**

### Color Palette
- **Forest Green (#1A5632)** — Primary. Headers, CTAs, nav active state
- **Forest Light (#2D8A4E)** — Secondary green accent
- **Gold (#C8962E)** — Primary accent. Buttons, badges, highlights
- **Gold Light (#F5D77A)** — Secondary gold for special emphasis
- **Cream (#FDFBF7)** — Background sections
- **Warm Dark (#1E1810)** — Footer, dark text — never pure `#000`

### Typography
- **Headings:** Playfair Display (serif, elegant)
- **Body:** Plus Jakarta Sans (clean geometric sans — Inter is banned per design skills)

### Navigation
- **Curved pill tabs** in a rounded-full container
- Active tab: forest green fill with white text
- Gold "Book Now" CTA button

### Services (Updated 2026-05-01)
1. Alcohol Catering
2. Coffee Catering
3. Mocktail Packages
4. Wine Tasting Experience
5. Mixology Classes (Atlanta local)
6. Bartender Training (4-week career program with festival placement)

### Mixology Classes Section
- Fun, energetic green section (#1A5632) with dot-pattern SVG background (no emojis)
- Groupon deals callout
- Class format pills: Private groups 6–20, Public workshops, Groupon deals from $29
- "What you'll learn" icon grid using Lucide icons
- 500+ students, 4.9 rating social proof + gold avatars

### Bartender Training Section
- Dark section (#1E1810) with gold line-pattern SVG background
- Career pathway positioning: "with a job at the end"
- Feature pills: Guaranteed job placement, Festival work experience, Industry certification
- Stats cards: 92% placement rate, 4-week program, 40+ recipes, 1 festival booked
- CTA links to `/bartender-training` dedicated page

### Design Principles
- Colorful, vibrant imagery (not monochromatic)
- Rounded corners everywhere (rounded-2xl, rounded-3xl)
- Warm, inviting feel — upscale but approachable
- Atlanta-local emphasis throughout

---

## Images

**Source:** Unsplash via `images.unsplash.com`
**Critical:** All URLs require `ixlib=rb-4.0.3` parameter. Without it, Unsplash returns 404.

**Helper:** `client/src/lib/images.ts` — 14 pre-built `IMG.*` constants

```
Format: https://images.unsplash.com/photo-{id}?ixlib=rb-4.0.3&auto=format&fit=crop&w={width}&q=80
```

| Constant | Photo ID | Subject |
|----------|----------|--------|
| `heroCocktails` | `1544148103-0773bf10d330` | Cocktails with garnish |
| `heroCoffee` | `1495474472287-4d71bcdd2085` | Coffee/latte art |
| `heroBartender` | `1514362545857-3bc16c4c7d1b` | Bartender at event |
| `heroWine` | `1470337458703-46ad1756a187` | Wine glasses |
| `wedding` | `1511795409834-ef04bbd61622` | Wedding reception |
| `corporate` | `1540575467063-178a50c2df87` | Corporate event |
| `privateParty` | `1530103862676-de8c9debad1d` | Private party |
| `teamBuilding` | `1528605248644-14dd04022da1` | Team activity |
| `mixologyClass` | `1572119865084-43c285814d63` | Mixology workshop |
| `mocktailCatering` | `1536935338788-846bb9981813` | Mocktail drinks |

---

## SEO Strategy

### On-Page
- **Title:** `BevPro — Beverage Catering & Mixology Classes | Atlanta` (50 chars)
- **H1:** Primary keywords in hero heading
- **14 FAQ items** on Home page (service area, pricing, dry-hire, classes, venues, insurance, custom menus, mocktails, differentiation, bartender training)
- **Service Area section:** 16 Atlanta neighborhoods listed
- **JSON-LD:** `LocalBusiness` schema with `OfferCatalog` (6 services), geo-coordinates, opening hours

### Target Keywords
- `mixology classes Atlanta`
- `bartender training Atlanta`
- `beverage catering Atlanta`
- `mobile bar service Atlanta`
- `alcohol catering Atlanta`
- `coffee catering Atlanta`
- `mocktail bar Atlanta`
- `wine tasting Atlanta`
- `corporate event bar Atlanta`
- `wedding bar service Atlanta`

## Social Media
- **Instagram:** https://www.instagram.com/mybevpro/
- **TikTok:** https://www.tiktok.com/@bevpro
- **LinkedIn:** placeholder (href="#")
- **X (Twitter):** placeholder (href="#")
- **Implementation:** `SocialLinks` component using `react-icons/fa6` — rendered in all page footers
- **Styling:** muted brown (#8B7355) → gold (#C8962E) on hover with site cubic-bezier, scale-110 on hover, scale-95 on active
- **Placeholders:** dimmed at 50% opacity, no `target="_blank"`, labeled "coming soon" in aria/title

## Remaining Opportunities
- Add `sitemap.xml`
- Blog/content hub for topical authority
- Google Business Profile optimization
- Real event photos (current: Unsplash stock)
- Set real LinkedIn and X URLs when accounts are created
