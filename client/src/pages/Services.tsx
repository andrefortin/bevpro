import { Button } from "@/components/ui/button";
import { Link, useLocation } from "wouter";
import {
  Wine,
  Coffee,
  Sparkles,
  GlassWater,
  GraduationCap,
  CheckCircle2,
  MapPin,
  Users,
  PartyPopper,
  Ticket,
  Martini,
  ChefHat,
  BookOpen,
  Star,
  Beer,
  Citrus,
  Briefcase,
  Music,
  Award,
  type LucideIcon,
} from "lucide-react";
import { useEffect, useRef } from "react";
import { IMG } from "@/lib/images";
import SocialLinks from "@/components/SocialLinks";

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
      { threshold: 0.12 }
    );
    el.querySelectorAll(".reveal-up").forEach((c) => obs.observe(c));
    return () => obs.disconnect();
  }, []);
  return ref;
}

function RevealSection({ children, className = "", ...rest }: { children: React.ReactNode; className?: string } & React.HTMLAttributes<HTMLElement>) {
  const ref = useScrollReveal();
  return <section ref={ref} className={className} {...rest}>{children}</section>;
}

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
      <div className="flex items-center gap-1 bg-white/85 backdrop-blur-xl rounded-full px-1.5 py-1.5 border border-black/5 shadow-diffuse">
        <Link href="/">
          <span className="text-lg font-bold cursor-pointer px-4 py-1.5 rounded-full" style={{ fontFamily: "'Playfair Display', serif", color: "#1A5632" }}>BevPro</span>
        </Link>
        <div className="w-px h-6 bg-black/8 mx-1" />
        {tabs.map((t) => (
          <Link key={t.path} href={t.path}>
            <span className={`nav-tab cursor-pointer ${loc === t.path ? "active" : ""}`}>{t.label}</span>
          </Link>
        ))}
        <div className="w-px h-6 bg-black/8 mx-1" />
        <Link href="/contact">
          <button className="group flex items-center gap-2 px-4 py-1.5 rounded-full font-semibold text-sm text-white active:scale-[0.98]" style={{ backgroundColor: "#C8962E" }}>
            Book Now
            <span className="btn-icon-circle light"><ChefHat className="w-3.5 h-3.5 text-white" strokeWidth={1.5} /></span>
          </button>
        </Link>
      </div>
    </nav>
  );
}

function CtaButton({ href, bg, text, icon: Icon }: { href: string; bg: string; text: string; icon: LucideIcon }) {
  return (
    <Link href={href}>
      <button className="group flex items-center gap-3 px-6 py-3 rounded-full font-semibold text-white active:scale-[0.98] text-sm" style={{ backgroundColor: bg }}>
        <span>{text}</span>
        <span className="btn-icon-circle light"><Icon className="w-3.5 h-3.5 text-white" strokeWidth={1.5} /></span>
      </button>
    </Link>
  );
}

function IconDot({ icon: Icon, color }: { icon: LucideIcon; color: string }) {
  return (
    <div className="w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0" style={{ backgroundColor: color }}>
      <Icon className="w-6 h-6 text-white" strokeWidth={1.5} />
    </div>
  );
}

export default function Services() {
  return (
    <div className="min-h-screen bg-white">
      <NavBar />

      {/* ── Header ── */}
      <section className="pt-36 pb-16 md:pt-44 md:pb-24 bg-[#FDFBF7]">
        <div className="container text-center">
          <div className="eyebrow bg-[#1A5632]/10 text-[#1A5632] mx-auto w-fit mb-6">
            <MapPin className="w-3 h-3" strokeWidth={1.5} />
            Atlanta &amp; Surrounding
          </div>
          <h1 style={{ color: "#1A5632" }} className="mb-4">Everything we do.</h1>
          <p className="text-[#6B5E4A] max-w-xl mx-auto leading-relaxed">
            Five services, one standard. Every bar, every pour, every class — run by professionals who care about the details.
          </p>
        </div>
      </section>

      {/* ── Alcohol Catering ── */}
      <RevealSection className="section-spacing bg-white">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="reveal-up">
              <IconDot icon={Wine} color="#1A5632" />
              <h2 style={{ color: "#1A5632" }} className="mt-6 mb-4">Alcohol Catering</h2>
              <p className="text-[#6B5E4A] mb-8 leading-relaxed max-w-md">
                Full bar service with premium spirits, craft cocktails, beer, and wine. Our bartenders arrive early, set up completely, serve with precision, and leave nothing behind.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  "Professional, certified bartenders",
                  "Complete bar setup — shakers, jiggers, glassware, garnishes",
                  "Custom cocktail menu designed for your event",
                  "Alcohol consultation — quantities and brand recommendations",
                  "Setup and breakdown — you handle nothing",
                ].map((f, i) => (
                  <div key={i} className="flex items-start gap-3 text-sm">
                    <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: "#2D8A4E" }} strokeWidth={1.5} />
                    <span className="text-[#6B5E4A]">{f}</span>
                  </div>
                ))}
              </div>
              <CtaButton href="/contact" bg="#1A5632" text="Book alcohol catering" icon={Wine} />
            </div>
            <div className="reveal-up" style={{ transitionDelay: "150ms" }}>
              <div className="card-shell">
                <img
                  src={IMG.alcoholCatering}
                  alt="Craft cocktails prepared with fresh ingredients"
                  className="rounded-[calc(2rem-0.375rem)] w-full h-[420px] object-cover"
                  loading="lazy"
                />
              </div>
            </div>
          </div>
        </div>
      </RevealSection>

      {/* ── Coffee Catering ── */}
      <RevealSection className="section-spacing bg-[#FDFBF7]">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="reveal-up order-2 md:order-1" style={{ transitionDelay: "150ms" }}>
              <div className="card-shell">
                <img
                  src={IMG.coffeeCatering}
                  alt="Artisanal espresso and latte art"
                  className="rounded-[calc(2rem-0.375rem)] w-full h-[420px] object-cover"
                  loading="lazy"
                />
              </div>
            </div>
            <div className="reveal-up order-1 md:order-2">
              <IconDot icon={Coffee} color="#6F4E37" />
              <h2 style={{ color: "#1A5632" }} className="mt-6 mb-4">Coffee Catering</h2>
              <p className="text-[#6B5E4A] mb-8 leading-relaxed max-w-md">
                Artisanal espresso bar with professional baristas. From morning meetings to late-night wedding sendoffs — lattes, cappuccinos, cold brew, and specialty drinks, served beautifully.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  "Professional baristas with specialty coffee training",
                  "Espresso, lattes, cappuccinos, cold brew, drip",
                  "Flavor syrups, alternative milks, custom drink menus",
                  "Commercial-grade equipment — full setup included",
                  "Perfect for breakfast events, break service, and night caps",
                ].map((f, i) => (
                  <div key={i} className="flex items-start gap-3 text-sm">
                    <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: "#2D8A4E" }} strokeWidth={1.5} />
                    <span className="text-[#6B5E4A]">{f}</span>
                  </div>
                ))}
              </div>
              <CtaButton href="/contact" bg="#6F4E37" text="Book coffee catering" icon={Coffee} />
            </div>
          </div>
        </div>
      </RevealSection>

      {/* ── Mocktail Packages ── */}
      <RevealSection className="section-spacing bg-white">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="reveal-up">
              <IconDot icon={Sparkles} color="#2D8A4E" />
              <h2 style={{ color: "#1A5632" }} className="mt-6 mb-4">Mocktail Packages</h2>
              <p className="text-[#6B5E4A] mb-8 leading-relaxed max-w-md">
                Craft zero-proof cocktails that look and taste exceptional. Fresh juices, house-made syrups, beautiful garnishes — everyone at your event deserves a premium pour.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  "Seasonal, chef-designed mocktail menus",
                  "Fresh-pressed juices, house syrups, exotic garnishes",
                  "Beautiful glassware and presentation",
                  "Optional pairing with your catering menu",
                  "Perfect for dry events, inclusive celebrations, and designated drivers",
                ].map((f, i) => (
                  <div key={i} className="flex items-start gap-3 text-sm">
                    <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: "#2D8A4E" }} strokeWidth={1.5} />
                    <span className="text-[#6B5E4A]">{f}</span>
                  </div>
                ))}
              </div>
              <CtaButton href="/contact" bg="#2D8A4E" text="Book mocktail bar" icon={Sparkles} />
            </div>
            <div className="reveal-up" style={{ transitionDelay: "150ms" }}>
              <div className="card-shell">
                <img
                  src={IMG.mocktailCatering}
                  alt="Beautifully presented mocktails with fresh garnishes"
                  className="rounded-[calc(2rem-0.375rem)] w-full h-[420px] object-cover"
                  loading="lazy"
                />
              </div>
            </div>
          </div>
        </div>
      </RevealSection>

      {/* ── Wine Tasting ── */}
      <RevealSection className="section-spacing bg-[#FDFBF7]">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="reveal-up order-2 md:order-1" style={{ transitionDelay: "150ms" }}>
              <div className="card-shell">
                <img
                  src={IMG.wineTasting}
                  alt="Wine tasting event with curated flights"
                  className="rounded-[calc(2rem-0.375rem)] w-full h-[420px] object-cover"
                  loading="lazy"
                />
              </div>
            </div>
            <div className="reveal-up order-1 md:order-2">
              <IconDot icon={GlassWater} color="#8B2252" />
              <h2 style={{ color: "#1A5632" }} className="mt-6 mb-4">Wine Tasting Experience</h2>
              <p className="text-[#6B5E4A] mb-8 leading-relaxed max-w-md">
                Guided tastings led by knowledgeable hosts. Curated flights, pairing notes, and a memorable experience for your guests — corporate events, private parties, celebrations.
              </p>
              <div className="space-y-4 mb-8">
                {[
                  "Guided tasting with a wine professional",
                  "Curated flights — reds, whites, sparkling, or mixed",
                  "Tasting notes, pairing guidance, and wine knowledge",
                  "Premium glassware and polished service",
                  "Great for team building, client entertainment, and toasts",
                ].map((f, i) => (
                  <div key={i} className="flex items-start gap-3 text-sm">
                    <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: "#2D8A4E" }} strokeWidth={1.5} />
                    <span className="text-[#6B5E4A]">{f}</span>
                  </div>
                ))}
              </div>
              <CtaButton href="/contact" bg="#8B2252" text="Book wine tasting" icon={GlassWater} />
            </div>
          </div>
        </div>
      </RevealSection>

      {/* ── Mixology Classes ── */}
      <RevealSection className="section-spacing relative overflow-hidden" style={{ backgroundColor: "#1A5632" }}>
        <div className="absolute inset-0 opacity-[0.06] pointer-events-none">
          <svg width="100%" height="100%">
            <defs>
              <pattern id="dots2" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
                <circle cx="30" cy="30" r="2" fill="white" />
                <circle cx="45" cy="15" r="1.5" fill="white" />
                <circle cx="15" cy="45" r="1.5" fill="white" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#dots2)" />
          </svg>
        </div>

        <div className="container relative z-10">
          <div className="text-center mb-14">
            <div className="eyebrow bg-white/15 text-[#F5D77A] mx-auto w-fit mb-6">
              <MapPin className="w-3 h-3" strokeWidth={1.5} />
              Atlanta Local
            </div>
            <h2 className="text-white mb-4" style={{ color: "#fff" }}>
              Mixology Classes
              <br />
              <span style={{ color: "#F5D77A" }}>Hands-on, high-energy, unforgettable.</span>
            </h2>
            <p className="text-[#D8CFB8] max-w-xl mx-auto leading-relaxed">
              Learn to shake, stir, and pour with confidence. Our workshops are built for anyone who wants to mix great drinks and have a great time doing it.
            </p>
          </div>

          {/* Class format cards */}
          <div className="grid md:grid-cols-3 gap-6 mb-14">
            {[
              { icon: Users, title: "Private Groups", desc: "Birthdays, date nights, team building. Book for 6–20 people — we come to you.", price: "$49/person" },
              { icon: PartyPopper, title: "Public Workshops", desc: "Join a scheduled class at partner venues around Atlanta. Meet people, learn together.", price: "$39/person" },
              { icon: Ticket, title: "Groupon Deals", desc: "Check Groupon for limited-time discounts on workshops and private classes.", price: "From $29" },
            ].map((card, i) => (
              <div key={i} className="reveal-up" style={{ transitionDelay: `${i * 100}ms` }}>
                <div className="h-full rounded-2xl p-8" style={{ backgroundColor: "rgba(255,255,255,0.08)", backdropFilter: "blur(4px)" }}>
                  <div className="w-12 h-12 rounded-2xl flex items-center justify-center mb-5" style={{ backgroundColor: "#F5D77A" }}>
                    <card.icon className="w-5 h-5" style={{ color: "#1A5632" }} strokeWidth={1.5} />
                  </div>
                  <h4 className="text-white font-bold mb-2">{card.title}</h4>
                  <p className="text-[#D8CFB8] text-sm mb-5 leading-relaxed">{card.desc}</p>
                  <p className="text-[#F5D77A] font-bold text-lg">{card.price}</p>
                </div>
              </div>
            ))}
          </div>

          {/* What you'll learn */}
          <div className="max-w-3xl mx-auto">
            <h4 className="text-white text-center font-semibold mb-8">What you will learn</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { icon: Martini, label: "Classic cocktails" },
                { icon: Beer, label: "Proper shaking" },
                { icon: Citrus, label: "Garnish technique" },
                { icon: GlassWater, label: "Layering & pouring" },
                { icon: Sparkles, label: "Fresh ingredients" },
                { icon: Wine, label: "Signature recipes" },
                { icon: BookOpen, label: "Recipe cards included" },
                { icon: Star, label: "Good times guaranteed" },
              ].map((item, i) => (
                <div
                  key={i}
                  className="rounded-xl px-4 py-3 text-center transition-transform hover:scale-105 duration-500"
                  style={{ backgroundColor: "rgba(255,255,255,0.07)" }}
                >
                  <item.icon className="w-4 h-4 mx-auto mb-2" style={{ color: "#F5D77A" }} strokeWidth={1.5} />
                  <span className="text-[#D8CFB8] text-xs font-medium">{item.label}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-12">
            <CtaButton href="/contact" bg="#C8962E" text="Book a class" icon={GraduationCap} />
            <a href="https://www.groupon.com" target="_blank" rel="noopener noreferrer">
              <button className="group flex items-center gap-3 px-6 py-3 rounded-full font-semibold text-sm active:scale-[0.98] border" style={{ borderColor: "#F5D77A", color: "#F5D77A" }}>
                Groupon deals
                <span className="btn-icon-circle light"><Ticket className="w-3.5 h-3.5" strokeWidth={1.5} style={{ color: "#F5D77A" }} /></span>
              </button>
            </a>
          </div>
        </div>
      </RevealSection>

      {/* ── Bartender Training ── */}
      <RevealSection className="section-spacing relative overflow-hidden" style={{ backgroundColor: "#1E1810" }}>
        <div className="absolute inset-0 opacity-[0.04] pointer-events-none">
          <svg width="100%" height="100%">
            <defs>
              <pattern id="lines2" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">
                <line x1="0" y1="0" x2="0" y2="40" stroke="#F5D77A" strokeWidth="1" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#lines2)" />
          </svg>
        </div>

        <div className="container relative z-10">
          <div className="text-center mb-14">
            <div className="eyebrow bg-[#C8962E]/20 text-[#F5D77A] mx-auto w-fit mb-6">
              <Award className="w-3 h-3" strokeWidth={1.5} />
              Career Track
            </div>
            <h2 className="text-white mb-4" style={{ color: "#fff" }}>
              Bartender Training
              <br />
              <span style={{ color: "#F5D77A" }}>Get trained. Get hired. Get behind the bar.</span>
            </h2>
            <p className="text-[#B8A88A] max-w-xl mx-auto leading-relaxed">
              A 4-week professional program that teaches you everything you need to work as a bartender — speed, accuracy, recipes, service flow, and certification. Graduate with a guaranteed job placement at a live festival.
            </p>
          </div>

          {/* Program structure */}
          <div className="grid md:grid-cols-3 gap-6 mb-14">
            {[
              { icon: BookOpen, title: "Week 1–2: Skills", desc: "Speed pouring, classic recipes, mixology fundamentals, bar setup and breakdown.", color: "#1A5632" },
              { icon: Award, title: "Week 3: Certification", desc: "Responsible alcohol service cert, customer service training, point-of-sale systems.", color: "#C8962E" },
              { icon: Music, title: "Week 4: Festival Placement", desc: "Work a live festival under supervision. Real bar, real guests, real experience.", color: "#8B2252" },
            ].map((card, i) => (
              <div key={i} className="reveal-up h-full" style={{ transitionDelay: `${i * 100}ms` }}>
                <div className="h-full rounded-2xl p-8" style={{ backgroundColor: "rgba(255,255,255,0.08)", backdropFilter: "blur(4px)" }}>
                  <div className="w-12 h-12 rounded-2xl flex items-center justify-center mb-5" style={{ backgroundColor: card.color }}>
                    <card.icon className="w-5 h-5 text-white" strokeWidth={1.5} />
                  </div>
                  <h4 className="text-white font-bold mb-2">{card.title}</h4>
                  <p className="text-[#D8CFB8] text-sm leading-relaxed">{card.desc}</p>
                </div>
              </div>
            ))}
          </div>

          {/* What you'll master */}
          <div className="max-w-3xl mx-auto">
            <h4 className="text-white text-center font-semibold mb-8">What you will master</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { icon: Martini, label: "40+ classic recipes" },
                { icon: Beer, label: "Speed pouring" },
                { icon: Citrus, label: "Garnish artistry" },
                { icon: GlassWater, label: "Layering & free-pour" },
                { icon: Briefcase, label: "Bar management" },
                { icon: Users, label: "Customer service" },
                { icon: Award, label: "Certification prep" },
                { icon: Music, label: "Festival experience" },
              ].map((item, i) => (
                <div
                  key={i}
                  className="rounded-xl px-4 py-3 text-center transition-transform hover:scale-105 duration-500"
                  style={{ backgroundColor: "rgba(255,255,255,0.07)" }}
                >
                  <item.icon className="w-4 h-4 mx-auto mb-2" style={{ color: "#F5D77A" }} strokeWidth={1.5} />
                  <span className="text-[#D8CFB8] text-xs font-medium">{item.label}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Price + CTA */}
          <div className="mt-12 text-center">
            <div className="inline-block rounded-2xl px-8 py-5 mb-8" style={{ backgroundColor: "rgba(255,255,255,0.08)" }}>
              <p className="text-[#B8A88A] text-sm mb-1">Program tuition</p>
              <p className="text-4xl font-bold" style={{ fontFamily: "'Playfair Display', serif", color: "#F5D77A" }}>$1,499</p>
              <p className="text-[#8B7355] text-xs mt-2">4 weeks · Includes certification · Guaranteed placement</p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <CtaButton href="/bartender-training" bg="#C8962E" text="View program details" icon={Briefcase} />
              <CtaButton href="/contact" bg="#1A5632" text="Apply for next cohort" icon={Award} />
            </div>
          </div>
        </div>
      </RevealSection>

      {/* ── CTA ── */}
      <section className="py-24 bg-[#FDFBF7] text-center">
        <div className="container">
          <h2 style={{ color: "#1A5632" }} className="mb-4">Ready to get started?</h2>
          <p className="text-[#6B5E4A] max-w-md mx-auto mb-8 leading-relaxed">
            Tell us about your event and we will build a proposal that fits.
          </p>
          <CtaButton href="/contact" bg="#1A5632" text="Request a quote" icon={BookOpen} />
        </div>
      </section>

      {/* ── Footer ── */}
      <footer style={{ backgroundColor: "#1E1810", color: "#FDFBF7" }} className="py-20">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
            <div>
              <h4 className="font-bold mb-4 text-lg" style={{ fontFamily: "'Playfair Display', serif", color: "#F5D77A" }}>BevPro</h4>
              <p className="text-[#B8A88A] text-sm leading-relaxed">Premium beverage catering.<br />Atlanta, Georgia.</p>
              <SocialLinks className="mt-5" />
            </div>
            <div>
              <h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Services</h5>
              <ul className="space-y-2.5 text-sm text-[#B8A88A]">
                <li>Alcohol Catering</li><li>Coffee Catering</li><li>Mocktail Packages</li><li>Wine Tasting</li><li>Mixology Classes</li><li>Bartender Training</li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Links</h5>
              <ul className="space-y-2.5 text-sm">
                <li><Link href="/packages"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Packages</span></Link></li>
                <li><Link href="/about"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">About</span></Link></li>
                <li><Link href="/contact"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Contact</span></Link></li>
                <li><a href="https://www.groupon.com" target="_blank" rel="noopener noreferrer" className="text-[#B8A88A] hover:text-white transition-colors duration-500">Groupon</a></li>
                <li><Link href="/terms"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Terms &amp; Conditions</span></Link></li>
                <li><Link href="/privacy"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Privacy Policy</span></Link></li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Contact</h5>
              <ul className="space-y-2.5 text-sm text-[#B8A88A]">
                <li><a href="mailto:hello@mybevpro.com" className="hover:text-white transition-colors duration-500">hello@mybevpro.com</a></li>
                <li><a href="tel:+14045551234" className="hover:text-white transition-colors duration-500">(404) 555-1234</a></li>
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
