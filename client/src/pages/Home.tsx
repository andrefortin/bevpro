import { Button } from "@/components/ui/button";
import { Link, useLocation } from "wouter";
import {
  Wine,
  Coffee,
  Sparkles,
  GlassWater,
  GraduationCap,
  Users,
  PartyPopper,
  MapPin,
  Star,
  Ticket,
  Martini,
  IceCream,
  Citrus,
  Beer,
  ChefHat,
  GlassWaterIcon,
  BookOpen,
  Clapperboard,
  Briefcase,
  Music,
  Award,
  type LucideIcon,
} from "lucide-react";
import { useEffect, useRef } from "react";
import { IMG } from "@/lib/images";
import SocialLinks from "@/components/SocialLinks";

/* ── Scroll reveal hook ── */
function useScrollReveal() {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    el.querySelectorAll(".reveal-up").forEach((c) => obs.observe(c));
    return () => obs.disconnect();
  }, []);
  return ref;
}

/* ── Reusable floating nav ── */
function NavBar() {
  const [loc] = useLocation();
  const tabs = [
    { label: "Home", path: "/" },
    { label: "Services", path: "/services" },
    { label: "Packages", path: "/packages" },
    { label: "About", path: "/about" },
    { label: "Contact", path: "/contact" },
  ];
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 flex justify-center pt-5">
      <div className="nav-pill">
        <Link href="/">
          <span
            className="text-lg font-bold cursor-pointer px-4 py-1.5 rounded-full"
            style={{
              fontFamily: "'Playfair Display', serif",
              color: "#1A5632",
            }}
          >
            BevPro
          </span>
        </Link>
        <div className="w-px h-6 bg-black/8 mx-1" />
        {tabs.map((t) => {
          const isHidden = t.label === "About";
          return (
          <Link key={t.path} href={t.path}>
            <span className={`nav-tab cursor-pointer ${isHidden ? "nav-tab-mobile-hidden" : ""} ${loc === t.path ? "active" : ""}`}>
              {t.label}
            </span>
          </Link>
          );
        })}
        <div className="w-px h-6 bg-black/8 mx-1" />
        <Link href="/contact">
          <button
            className="group flex items-center gap-2 px-4 py-1.5 rounded-full font-semibold text-sm text-white active:scale-[0.98]"
            style={{ backgroundColor: "#C8962E" }}
          >
            Book Now
            <span className="btn-icon-circle light">
              <ChefHat className="w-3.5 h-3.5 text-white" strokeWidth={1.5} />
            </span>
          </button>
        </Link>
      </div>
    </nav>
  );
}

/* ── Section wrapper with scroll reveal ── */
function RevealSection({ children, className = "", ...rest }: { children: React.ReactNode; className?: string } & React.HTMLAttributes<HTMLElement>) {
  const ref = useScrollReveal();
  return (
    <section ref={ref} className={className} {...rest}>
      {children}
    </section>
  );
}

/* ── Double-bezel card ── */
function BezelCard({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div className="card-shell">
      <div className={`card-core ${className}`}>{children}</div>
    </div>
  );
}

/* ── Service icon dot ── */
function IconDot({ icon: Icon, color }: { icon: LucideIcon; color: string }) {
  return (
    <div
      className="w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0"
      style={{ backgroundColor: color }}
    >
      <Icon className="w-5 h-5 text-white" strokeWidth={1.5} />
    </div>
  );
}

/* ── Button-in-Button CTA ── */
function CtaButton({
  href,
  bg,
  text,
  children,
  icon: Icon,
}: {
  href: string;
  bg: string;
  text: string;
  children?: React.ReactNode;
  icon?: LucideIcon;
}) {
  const content = (
    <button
      className="group flex items-center gap-3 px-6 py-3 rounded-full font-semibold text-white active:scale-[0.98]"
      style={{ backgroundColor: bg }}
    >
      <span>{children || text}</span>
      {Icon && (
        <span className="btn-icon-circle light">
          <Icon className="w-3.5 h-3.5 text-white" strokeWidth={1.5} />
        </span>
      )}
    </button>
  );
  return <Link href={href}>{content}</Link>;
}

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <NavBar />

      {/* ── Hero — Editorial split, colorful imagery ── */}
      <RevealSection className="pt-32 pb-24 md:pt-44 md:pb-36 bg-[#FDFBF7]">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-12 md:gap-20 items-center">
            <div className="reveal-up">
              <div className="eyebrow bg-[#1A5632]/10 text-[#1A5632] mb-6">
                <MapPin className="w-3 h-3" strokeWidth={1.5} />
                Atlanta &amp; Surrounding
              </div>
              <h1 style={{ color: "#1A5632" }} className="mb-6">
                Atlanta beverage catering &amp; mixology classes that <span style={{ color: "#C8962E" }}>feel effortless.</span>
              </h1>
              <p className="text-base text-[#6B5E4A] mb-8 max-w-lg leading-relaxed">
                BevPro is Georgia&apos;s premium mobile bar catering company. We specialize in alcohol catering, coffee bars, mocktail packages, wine tastings, and hands-on mixology classes — all delivered with precision and care nationwide.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <CtaButton href="/services" bg="#1A5632" text="Explore Services" icon={Wine} />
                <Link href="/packages">
                  <button
                    className="group flex items-center gap-3 px-6 py-3 rounded-full font-semibold text-sm active:scale-[0.98] border"
                    style={{ borderColor: "#C8962E", color: "#C8962E" }}
                  >
                    View Packages
                    <span className="btn-icon-circle" style={{ background: "rgba(200,150,46,0.1)" }}>
                      <BookOpen className="w-3.5 h-3.5" strokeWidth={1.5} style={{ color: "#C8962E" }} />
                    </span>
                  </button>
                </Link>
              </div>
            </div>

            {/* Hero image grid — colorful, no dark overlay */}
            <div className="reveal-up" style={{ transitionDelay: "150ms" }}>
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-3">
                  <div className="rounded-2xl overflow-hidden shadow-lg">
                    <img src={IMG.heroCocktails} alt="Craft cocktail with fresh citrus garnish and edible flowers" className="w-full h-40 object-cover" loading="lazy" />
                  </div>
                  <div className="rounded-2xl overflow-hidden shadow-lg">
                    <img src={IMG.heroCoffee} alt="Professional barista pouring latte art at coffee catering event" className="w-full h-40 object-cover" loading="lazy" />
                  </div>
                </div>
                <div className="space-y-3 pt-6">
                  <div className="rounded-2xl overflow-hidden shadow-lg">
                    <img src={IMG.heroBartender} alt="Professional bartender crafting drinks at a corporate event in Atlanta" className="w-full h-52 object-cover" loading="lazy" />
                  </div>
                  <div className="rounded-2xl overflow-hidden shadow-lg">
                    <img src={IMG.heroWine} alt="Wine glasses on an elegantly set table at golden hour event" className="w-full h-32 object-cover" loading="lazy" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </RevealSection>

      {/* ── Who We Serve — Event types with images ── */}
      <RevealSection className="bg-white py-16 md:py-24">
        <div className="container">
          <div className="mb-12 text-center">
            <div className="eyebrow bg-[#C8962E]/10 text-[#C8962E] mx-auto w-fit mb-4">
              Who we serve
            </div>
            <h2 style={{ color: "#1A5632" }} className="mb-3">
              Event bar catering for every occasion.
            </h2>
            <p className="text-[#6B5E4A] max-w-2xl mx-auto text-sm leading-relaxed">
              From weddings to corporate galas, birthdays to team-building workshops — BevPro brings the bar to your venue. Alcohol catering, coffee bars, mocktail stations, wine tastings, and mixology classes, all delivered by certified professional bartenders.
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { img: IMG.wedding, label: "Weddings", desc: "Signature cocktails for your big day" },
              { img: IMG.corporate, label: "Corporate Events", desc: "Professional bar service at scale" },
              { img: IMG.privateParty, label: "Private Parties", desc: "Birthdays, anniversaries, milestones" },
              { img: IMG.teamBuilding, label: "Team Building", desc: "Mixology classes that bring teams together" },
            ].map((item, i) => (
              <div key={i} className="reveal-up group cursor-pointer" style={{ transitionDelay: `${i * 80}ms` }}>
                <div className="rounded-2xl overflow-hidden shadow-md mb-3 aspect-[4/3]">
                  <img
                    src={item.img}
                    alt={`${item.label} — ${item.desc} by BevPro Atlanta`}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]"
                    loading="lazy"
                  />
                </div>
                <h3 className="font-bold text-sm" style={{ color: "#1A5632" }}>{item.label}</h3>
                <p className="text-xs text-[#8B7355]">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </RevealSection>

      {/* ── Atlanta Service Area — Local SEO ── */}
      <RevealSection className="bg-[#FDFBF7] py-20 md:py-28">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="reveal-up">
              <div className="eyebrow bg-[#1A5632]/10 text-[#1A5632] mb-4">
                <MapPin className="w-3 h-3" strokeWidth={1.5} />
                Service Area
              </div>
              <h2 style={{ color: "#1A5632" }} className="mb-4">
                Based in Georgia, serving nationwide.
              </h2>
              <p className="text-[#6B5E4A] mb-6 leading-relaxed">
                BevPro is based in Atlanta, Georgia and provides mobile bar catering, coffee catering, mocktail packages, wine tasting experiences, mixology classes, and bartender training — with nationwide availability. We bring everything to your venue — you focus on your guests.
              </p>
              <div className="grid grid-cols-2 gap-3 text-sm">
                {[
                  "Fulton", "Gwinnett", "Cobb", "DeKalb",
                  "Forsyth", "Cherokee", "Douglas", "And Beyond…",
                ].map((area) => (
                  <div key={area} className="flex items-center gap-2 text-[#6B5E4A]">
                    <MapPin className="w-3 h-3 flex-shrink-0" style={{ color: "#2D8A4E" }} strokeWidth={1.5} />
                    {area}
                  </div>
                ))}
              </div>
              <p className="text-xs text-[#8B7355] mt-6">
                Nationwide travel available on request. Call us at <a href="tel:+16788881505" className="underline" style={{ color: "#2D8A4E" }}>(678) 888-1505</a> or email <a href="mailto:hello@mybevpro.com" className="underline" style={{ color: "#2D8A4E" }}>hello@mybevpro.com</a> to confirm availability for your specific venue.
              </p>
            </div>
            <div className="reveal-up" style={{ transitionDelay: "150ms" }}>
              <div className="card-shell">
                <div className="card-core !p-4">
                  <img
                    src="/google-maps-atlanta-ga.png"
                    alt="Google Maps view of Atlanta Georgia — BevPro beverage catering service area covering Fulton, Gwinnett, Cobb, DeKalb, Forsyth, Cherokee, Douglas, and beyond"
                    className="rounded-2xl w-full h-auto"
                    loading="lazy"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </RevealSection>

      {/* ── Services — SEO-optimized bento grid ── */}
      <RevealSection className="section-spacing bg-white">
        <div className="container">
          <div className="mb-16">
            <div className="eyebrow bg-[#C8962E]/10 text-[#C8962E] mb-4">
              Atlanta beverage services
            </div>
            <h2 style={{ color: "#1A5632" }} className="mb-3">
              Five ways we serve.
            </h2>
            <p className="text-[#6B5E4A] max-w-xl">
              From mobile bar catering to career bartender training — every service is delivered by certified professionals who treat your event like their own. Based in Georgia, available nationwide.
            </p>
          </div>

          {/* Bento grid: md:grid-cols-3, Alcohol tall card row-span-2 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                icon: Wine,
                title: "Alcohol Catering",
                desc: "Atlanta's trusted mobile bar service. Premium spirits, craft cocktails, beer, and wine — served by certified bartenders at weddings, corporate events, and private parties across Buckhead, Midtown, and beyond.",
                color: "#1A5632",
                span: "md:col-span-2 md:row-span-2",
                tall: true,
                href: "/services",
              },
              {
                icon: Coffee,
                title: "Coffee Catering",
                desc: "Artisanal espresso bar for Atlanta events. Professional baristas, latte art, cold brew, and specialty drinks — perfect for morning conferences, wedding sendoffs, and corporate breakfasts.",
                color: "#6F4E37",
                span: "md:col-span-1",
                href: "/services",
              },
              {
                icon: Sparkles,
                title: "Mocktail Packages",
                desc: "Craft zero-proof cocktails for Atlanta celebrations. Fresh juices, house-made syrups, seasonal garnishes — premium drinks for every guest, with or without alcohol.",
                color: "#2D8A4E",
                span: "md:col-span-1",
                href: "/services",
              },
              {
                icon: GlassWater,
                title: "Wine Tasting",
                desc: "Guided wine tasting experiences in Atlanta. Curated flights, food pairing notes, and sommelier-led sessions for corporate events, private parties, and special occasions.",
                color: "#8B2252",
                span: "md:col-span-1",
                href: "/services",
              },
              {
                icon: GraduationCap,
                title: "Mixology Classes",
                desc: "Hands-on mixology classes — we come to your location. Private groups, public workshops, and Groupon deals. Learn to craft signature cocktails in a 2-hour session — perfect for team building and date nights.",
                color: "#C8962E",
                span: "md:col-span-1",
                badge: "Most Popular",
                href: "/services",
              },
            ].map((s, i) => (
              <div
                key={i}
                className={`card-shell ${s.span} reveal-up`}
                style={{ transitionDelay: `${i * 80}ms` }}
              >
                <div
                  className={`card-core h-full flex flex-col ${s.tall ? "justify-between" : ""}`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <IconDot icon={s.icon} color={s.color} />
                      {s.badge && (
                        <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-[#1A5632] text-white">
                          {s.badge}
                        </span>
                      )}
                    </div>
                    <Link href={s.href}>
                      <h3 className="mb-2 hover:underline cursor-pointer" style={{ color: "#1A5632" }}>
                        {s.title}
                      </h3>
                    </Link>
                    <p className="text-[#6B5E4A] text-sm leading-relaxed">{s.desc}</p>
                  </div>
                  {s.tall && (
                    <div className="mt-6 grid grid-cols-2 gap-2">
                      {[
                        { icon: Martini, label: "Craft cocktails" },
                        { icon: Beer, label: "Premium beer & wine" },
                        { icon: Citrus, label: "Setup & breakdown" },
                        { icon: MapPin, label: "Atlanta-wide service" },
                      ].map((item, j) => (
                        <div
                          key={j}
                          className="flex items-center gap-2 text-xs font-medium text-[#6B5E4A] bg-[#F5F0E8] rounded-xl px-3 py-2"
                        >
                          <item.icon className="w-3.5 h-3.5" strokeWidth={1.5} style={{ color: s.color }} />
                          {item.label}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Trust bar — local SEO + social proof */}
          <div className="mt-14 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            {[
              { stat: "500+", label: "Events served" },
              { stat: "95%", label: "Client rebook rate" },
              { stat: "8+", label: "Georgia counties" },
              { stat: "10+", label: "Years in business" },
            ].map((item, i) => (
              <div key={i} className="reveal-up rounded-2xl bg-[#FDFBF7] border border-[#E8DFD0] px-4 py-5" style={{ transitionDelay: `${i * 80}ms` }}>
                <div className="text-2xl font-bold mb-1" style={{ fontFamily: "'Playfair Display', serif", color: "#C8962E" }}>{item.stat}</div>
                <div className="text-xs text-[#6B5E4A] font-medium">{item.label}</div>
              </div>
            ))}
          </div>
        </div>
      </RevealSection>

      {/* ── Mixology Classes — Energy without emojis ── */}
      <RevealSection className="section-spacing relative overflow-hidden" style={{ backgroundColor: "#1A5632" }}>
        {/* Abstract pattern — no emoji, just geometry */}
        <div className="absolute inset-0 opacity-[0.06] pointer-events-none">
          <svg width="100%" height="100%">
            <defs>
              <pattern id="dots" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
                <circle cx="30" cy="30" r="2" fill="white" />
                <circle cx="45" cy="15" r="1.5" fill="white" />
                <circle cx="15" cy="45" r="1.5" fill="white" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#dots)" />
          </svg>
        </div>

        <div className="container relative z-10">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="reveal-up">
              <div className="eyebrow bg-white/15 text-[#F5D77A] mb-6">
                <Star className="w-3 h-3" strokeWidth={1.5} fill="#F5D77A" />
                Most requested
              </div>
              <h2 className="text-white mb-4" style={{ color: "#fff" }}>
                Mixology classes,{" "}
                <span style={{ color: "#F5D77A" }}>we come to you.</span>
              </h2>
              <p className="text-[#D8CFB8] mb-8 leading-relaxed max-w-md">
                Hands-on workshops at your location. You shake, stir, and pour your way to cocktail
                confidence. No experience required. We bring the tools, the ingredients, and
                the energy to you — you just bring your crew.
              </p>

              {/* Class format pills */}
              <div className="flex flex-wrap gap-3 mb-8">
                {[
                  { icon: Users, label: "Private groups 6–20" },
                  { icon: PartyPopper, label: "Public workshops" },
                  { icon: Ticket, label: "Groupon deals from $29" },
                ].map((f, i) => (
                  <div
                    key={i}
                    className="flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium"
                    style={{ backgroundColor: "rgba(255,255,255,0.1)", color: "#E8DFD0" }}
                  >
                    <f.icon className="w-3.5 h-3.5" strokeWidth={1.5} style={{ color: "#F5D77A" }} />
                    {f.label}
                  </div>
                ))}
              </div>

              <div className="flex items-center gap-5 mb-8">
                <div className="flex -space-x-3">
                  {["#F5D77A", "#E0C060", "#C8962E", "#D4A843"].map((c, i) => (
                    <div
                      key={i}
                      className="w-10 h-10 rounded-full border-2 flex items-center justify-center text-xs font-bold"
                      style={{ borderColor: "#1A5632", backgroundColor: c, color: "#1A5632" }}
                    >
                      {String.fromCharCode(65 + i)}
                    </div>
                  ))}
                </div>
                <div>
                  <div className="flex gap-0.5 mb-0.5">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className="w-4 h-4" fill="#F5D77A" strokeWidth={0} />
                    ))}
                  </div>
                  <p className="text-xs text-[#D8CFB8]">500+ students enrolled — 4.9 rating</p>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <CtaButton href="/contact" bg="#C8962E" text="Book a class" icon={GraduationCap} />
                <a href="https://www.groupon.com" target="_blank" rel="noopener noreferrer">
                  <button
                    className="group flex items-center gap-3 px-6 py-3 rounded-full font-semibold text-sm active:scale-[0.98] border"
                    style={{ borderColor: "#F5D77A", color: "#F5D77A" }}
                  >
                    Groupon deals
                    <span className="btn-icon-circle light">
                      <Ticket className="w-3.5 h-3.5" strokeWidth={1.5} style={{ color: "#F5D77A" }} />
                    </span>
                  </button>
                </a>
              </div>
            </div>

            {/* Image + floating badge */}
            <div className="relative reveal-up" style={{ transitionDelay: "200ms" }}>
              <img
                src={IMG.mixologyClass}
                alt="Mixology class in action"
                className="rounded-[2.5rem] w-full h-[460px] object-cover shadow-diffuse"
                loading="lazy"
              />
              <div
                className="absolute -top-4 -left-4 bg-white rounded-2xl shadow-diffuse px-5 py-4 flex items-center gap-3"
              >
                <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ backgroundColor: "#1A5632" }}>
                  <Martini className="w-5 h-5 text-white" strokeWidth={1.5} />
                </div>
                <div>
                  <p className="font-bold text-sm" style={{ color: "#1A5632" }}>
                    Mojito mastery
                  </p>
                  <p className="text-xs text-[#8B7355]">Student favorite &rarr;</p>
                </div>
              </div>
              <div
                className="absolute -bottom-4 -right-4 rounded-2xl shadow-diffuse px-6 py-4"
                style={{ backgroundColor: "#C8962E" }}
              >
                <p className="text-white font-bold text-sm">$49 per person</p>
                <p className="text-[#FDFBF7] text-xs mt-0.5">or find us on Groupon</p>
              </div>
            </div>
          </div>
        </div>
      </RevealSection>

      {/* ── Testimonials — Double-bezel ── */}
      <RevealSection className="section-spacing bg-[#FDFBF7]">
        <div className="container">
          <div className="mb-16 text-center">
            <div className="eyebrow bg-[#C8962E]/10 text-[#C8962E] mb-4 mx-auto w-fit">
              Client notes
            </div>
            <h2 style={{ color: "#1A5632" }} className="mb-3">
              Trusted by Atlanta event hosts.
            </h2>
            <p className="text-[#6B5E4A] max-w-lg mx-auto text-sm mt-2">
              500+ events served across the metro area. Here is what our clients say about BevPro beverage catering and mixology classes.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                quote: "The mixology workshop was the highlight of our team offsite. Everyone walked away mixing drinks like they'd been doing it for years. Unforgettable afternoon.",
                author: "Jessica Moretti",
                role: "Operations Director, Atlanta fintech",
              },
              {
                quote: "BevPro ran the bar at our wedding — signature cocktails, coffee bar for the late-night crowd, zero stress. Our guests still bring it up.",
                author: "David & Rachel Park",
                role: "Married October 2025, Buckhead",
              },
              {
                quote: "Found the Groupon deal for a class and now we book BevPro for every quarterly event. Consistency you can count on.",
                author: "Marcus Tolliver",
                role: "Corporate Events, Midtown 400",
              },
            ].map((t, i) => (
              <div key={i} className="card-shell reveal-up" style={{ transitionDelay: `${i * 100}ms` }}>
                <div className="card-core">
                  <div className="flex gap-1 mb-4">
                    {[...Array(5)].map((_, j) => (
                      <Star key={j} className="w-3.5 h-3.5" fill="#C8962E" strokeWidth={0} />
                    ))}
                  </div>
                  <p className="text-[#6B5E4A] text-sm leading-relaxed mb-6 italic">
                    &ldquo;{t.quote}&rdquo;
                  </p>
                  <div className="flex items-center gap-3">
                    <div
                      className="w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold"
                      style={{ backgroundColor: "#1A5632", color: "#FDFBF7" }}
                    >
                      {t.author.charAt(0)}
                    </div>
                    <div>
                      <p className="text-sm font-semibold" style={{ color: "#1A5632" }}>
                        {t.author}
                      </p>
                      <p className="text-xs text-[#8B7355]">{t.role}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </RevealSection>

      {/* ── Groupon banner ── */}
      <section className="py-24 relative overflow-hidden" style={{ backgroundColor: "#C8962E" }}>
        <div className="absolute inset-0 opacity-[0.07] pointer-events-none">
          <svg width="100%" height="100%">
            <defs>
              <pattern id="stripes" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
                <line x1="0" y1="0" x2="0" y2="40" stroke="white" strokeWidth="1" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#stripes)" />
          </svg>
        </div>
        <div className="container relative z-10 text-center">
          <div className="eyebrow bg-white/20 text-white mx-auto w-fit mb-6">
            <Ticket className="w-3 h-3" strokeWidth={1.5} />
            Limited offers
          </div>
          <h2 className="text-white mb-4" style={{ color: "#fff" }}>
            Find BevPro on Groupon.
          </h2>
          <p className="text-[#FDFBF7] mb-8 max-w-lg mx-auto leading-relaxed">
            Rotating deals on mixology classes and cocktail experiences. New offers drop monthly — grab yours before they sell out.
          </p>
          <a href="https://www.groupon.com" target="_blank" rel="noopener noreferrer">
            <button
              className="group flex items-center gap-3 mx-auto px-8 py-4 rounded-full font-bold text-base active:scale-[0.98]"
              style={{ backgroundColor: "#1A5632", color: "#fff" }}
            >
              View Groupon deals
              <span className="btn-icon-circle light">
                <Ticket className="w-3.5 h-3.5 text-white" strokeWidth={1.5} />
              </span>
            </button>
          </a>
        </div>
      </section>

      {/* ── FAQ — SEO-focused ── */}
      <RevealSection className="section-spacing bg-white">
        <div className="container max-w-3xl">
          <div className="mb-14 text-center">
            <div className="eyebrow bg-[#1A5632]/10 text-[#1A5632] mx-auto w-fit mb-4">
              Got questions?
            </div>
            <h2 style={{ color: "#1A5632" }} className="mb-3">
              Atlanta beverage catering FAQ.
            </h2>
            <p className="text-[#6B5E4A] text-sm max-w-lg mx-auto">
              Answers to common questions about our mobile bar service, mixology classes, bartender training, and event catering nationwide.
            </p>
          </div>
          <div className="space-y-8">
            {[
              {
                q: "What areas does BevPro serve?",
                a: "We are based in Atlanta, Georgia and serve the metro area — Fulton, Gwinnett, Cobb, DeKalb, Forsyth, Cherokee, Douglas, and surrounding communities. Nationwide travel is available on request. Contact us to confirm availability for your specific venue.",
              },
              {
                q: "What types of events do you cater?",
                a: "We cater weddings, corporate events, private parties, galas, fundraisers, product launches, holiday parties, team-building workshops, and more. Our mixology classes are especially popular for corporate team-building events, birthday parties, and date nights.",
              },
              {
                q: "How does alcohol purchasing work with the dry-hire model?",
                a: "Dry-hire means you purchase alcohol directly from your preferred supplier at retail price. We provide expert recommendations on brands, types, and quantities based on your guest count and event style. You pay the supplier directly — we charge only for our bar service, with zero markup on alcohol. This gives you full control over your budget and brand selection.",
              },
              {
                q: "Are your mixology classes suitable for complete beginners?",
                a: "Absolutely. Our classes are designed for all skill levels — from people who have never held a shaker to experienced home enthusiasts. All tools, ingredients, and recipe cards are provided. You just show up ready to learn and have fun. Many students find us through Groupon for their first class.",
              },
              {
                q: "How far in advance should I book?",
                a: "We recommend booking 4–6 weeks ahead for events to ensure availability and allow time for consultation and planning. For mixology classes, 2–3 weeks notice is ideal. For bartender training, 4 weeks minimum due to festival placement scheduling. Rush requests are accommodated when possible — reach out and we will do our best to fit you in.",
              },
              {
                q: "What is included in your bar service packages?",
                a: "Every package includes professional bartenders, premium bar equipment, glassware, garnishes, mixers, ice, full setup before your event, and complete breakdown afterward. Higher-tier packages add delivery coordination, custom cocktail menu design, and on-site bar management. Alcohol is always purchased separately by you — we handle the rest.",
              },
              {
                q: "Do you carry insurance and licenses?",
                a: "Yes. BevPro carries full liability insurance and all bartenders hold required certifications. We operate in compliance with Georgia state and local regulations. Certificates of insurance can be provided to your venue upon request.",
              },
              {
                q: "Can you create custom cocktail menus for branded events?",
                a: "Definitely. We design signature cocktail menus tailored to your event theme, company branding, or personal preferences. Custom menus are available as an add-on with our Premium and Grand packages, or can be added to any booking.",
              },
              {
                q: "How much does beverage catering cost?",
                a: "Our bar service packages start at $1,200 for the Essential tier (50–100 guests, 1 bartender) and go up to custom quotes for Grand Celebration events (250+ guests). Alcohol is purchased separately by you at retail cost — we charge only for our professional bartending and bar management service. Coffee catering, mocktail packages, wine tastings, mixology classes, and bartender training are priced individually. Request a quote for a detailed proposal tailored to your event.",
              },
              {
                q: "What makes BevPro different from other bar services?",
                a: "Three things set us apart. First, our dry-hire model — you control your alcohol budget with zero markup from us. Second, our bartenders are career professionals, not temporary gig workers. Third, we are a full-service beverage company — alcohol catering, coffee, mocktails, wine tastings, mixology classes, and bartender training all under one roof. One call, one team, one standard of excellence.",
              },
              {
                q: "Do you offer non-alcoholic options for events?",
                a: "Yes. Our mocktail packages feature craft zero-proof cocktails made with fresh juices, house-made syrups, and beautiful garnishes. Our coffee catering provides a full espresso bar experience. We believe every guest deserves a premium drink, with or without alcohol. Mocktail stations are available as a standalone service or as an add-on to any alcohol catering package.",
              },
              {
                q: "Can you work with my venue or event planner?",
                a: "Absolutely. We coordinate directly with venues, wedding planners, corporate event coordinators, and caterers. We can provide certificates of insurance, floor plans for bar placement, and attend site walkthroughs upon request. Our goal is to make your planner&apos;s job easier — not harder.",
              },
              {
                q: "What is included in a mixology class?",
                a: "Each 2-hour mixology class includes all tools (shakers, jiggers, strainers, glassware), all ingredients (spirits, mixers, fresh garnishes), printed recipe cards for every drink you learn, and hands-on instruction from a professional bartender. You choose how many drinks you want to learn. We come to your location — no travel on your end. Classes are available as private bookings for groups of 6–20, or you can join a public workshop at a partner venue. Groupon deals are available for select sessions.",
              },
              {
                q: "How does the bartender training program work?",
                a: "Our Bartender in a Day program is a super intense 1-day course. You&apos;ll learn the top skills needed to get your foot in the door — speed, accuracy, and recipe mastery. Taught by bartenders who have hired hundreds and know exactly what employers are looking for. Job placement assistance is available upon completion.",
              },
            ].map((faq, i) => (
              <div key={i} className="reveal-up" style={{ transitionDelay: `${i * 60}ms` }}>
                <h4
                  className="font-bold text-base mb-2"
                  style={{ color: "#1A5632", fontFamily: "'Plus Jakarta Sans', sans-serif" }}
                >
                  {faq.q}
                </h4>
                <p className="text-[#6B5E4A] text-sm leading-relaxed">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </RevealSection>

      {/* ── Footer ── */}
      <footer style={{ backgroundColor: "#1E1810", color: "#FDFBF7" }} className="py-20">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
            <div>
              <h4
                className="font-bold mb-4 text-lg"
                style={{ fontFamily: "'Playfair Display', serif", color: "#F5D77A" }}
              >
                BevPro
              </h4>
              <p className="text-[#B8A88A] text-sm leading-relaxed">
                Premium beverage catering.
                <br />
                Atlanta, Georgia.
              </p>
              <SocialLinks className="mt-5" />
            </div>
            <div>
              <h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">
                Services
              </h5>
              <ul className="space-y-2.5 text-sm text-[#B8A88A]">
                <li>Alcohol Catering</li>
                <li>Coffee Catering</li>
                <li>Mocktail Packages</li>
                <li>Wine Tasting</li>
                <li>Mixology Classes</li>
                
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">
                Links
              </h5>
              <ul className="space-y-2.5 text-sm">
                <li>
                  <Link href="/packages">
                    <span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">
                      Packages
                    </span>
                  </Link>
                </li>
                <li>
                  <Link href="/about">
                    <span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">
                      About
                    </span>
                  </Link>
                </li>
                <li>
                  <Link href="/contact">
                    <span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">
                      Contact
                    </span>
                  </Link>
                </li>
                <li>
                  <Link href="/bartender-training">
                    <span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">
                      Bartender Training
                    </span>
                  </Link>
                </li>
                <li>
                  <a
                    href="https://www.groupon.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[#B8A88A] hover:text-white transition-colors duration-500"
                  >
                    Groupon
                  </a>
                </li>
                <li>
                  <Link href="/terms">
                    <span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">
                      Terms &amp; Conditions
                    </span>
                  </Link>
                </li>
                <li>
                  <Link href="/privacy">
                    <span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">
                      Privacy Policy
                    </span>
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">
                Contact
              </h5>
              <ul className="space-y-2.5 text-sm text-[#B8A88A]">
                <li>
                  <a href="mailto:hello@mybevpro.com" className="hover:text-white transition-colors duration-500">
                    hello@mybevpro.com
                  </a>
                </li>
                <li>
                  <a href="tel:+16788881505" className="hover:text-white transition-colors duration-500">
                    (678) 888-1505
                  </a>
                </li>
                <li>Atlanta, GA</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-white/10 pt-8 text-center text-xs text-[#6B5E4A]">
            <p>&copy; 2026 BevPro LLC. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
