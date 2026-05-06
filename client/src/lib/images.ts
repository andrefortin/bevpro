/**
 * BevPro image sources — Unsplash Photos with required ixlib parameter.
 * Format: https://images.unsplash.com/photo-{id}?ixlib=rb-4.0.3&auto=format&fit=crop&w={width}&q=80
 * All URLs verified working (HTTP 200) as of 2026-05-03.
 */

const U = (id: string, w = 800) =>
  `https://images.unsplash.com/photo-${id}?ixlib=rb-4.0.3&auto=format&fit=crop&w=${w}&q=80`;

export const IMG = {
  heroCocktails:    U("1544148103-0773bf10d330", 600),
  heroCoffee:       U("1495474472287-4d71bcdd2085", 600),
  heroBartender:    U("1514362545857-3bc16c4c7d1b", 600),
  heroWine:         U("1470337458703-46ad1756a187", 600),
  wedding:          U("1511795409834-ef04bbd61622", 600),
  corporate:        U("1540575467063-178a50c2df87", 600),
  privateParty:     U("1530103862676-de8c9debad1d", 600),
  teamBuilding:     U("1528605248644-14dd04022da1", 600),
  mixologyClass:     U("1572119865084-43c285814d63", 700),
  alcoholCatering:  U("1544148103-0773bf10d330", 800),
  coffeeCatering:   U("1495474472287-4d71bcdd2085", 800),
  mocktailCatering: U("1536935338788-846bb9981813", 800),
  wineTasting:      U("1470337458703-46ad1756a187", 800),
  aboutTeam:        U("1514362545857-3bc16c4c7d1b", 800),
};
