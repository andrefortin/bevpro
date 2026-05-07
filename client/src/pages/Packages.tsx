import { Button } from "@/components/ui/button";
import { Link, useLocation } from "wouter";
import { CheckCircle2, Sparkles, Wine, Martini, BookOpen, ChefHat, type LucideIcon } from "lucide-react";
import { useEffect, useRef } from "react";
import SocialLinks from "@/components/SocialLinks";

function useScrollReveal() {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) { entry.target.classList.add("visible"); obs.unobserve(entry.target); }
        });
      },
      { threshold: 0.12 }
    );
    el.querySelectorAll(".reveal-up").forEach((c) => obs.observe(c));
    return () => obs.disconnect();
  }, []);
  return ref;
}

function RevealSection({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  const ref = useScrollReveal();
  return <section ref={ref} className={className}>{children}</section>;
}

function NavBar() {
  const [loc] = useLocation();
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 flex justify-center pt-5">
      <div className="nav-pill">
        <Link href="/"><span className="text-lg font-bold cursor-pointer px-4 py-1.5 rounded-full" style={{ fontFamily: "'Playfair Display', serif", color: "#1A5632" }}>BevPro</span></Link>
        <div className="w-px h-6 bg-black/8 mx-1" />
        {[{ label: "Home", path: "/" }, { label: "Services", path: "/services" }, { label: "Packages", path: "/packages" }, { label: "About", path: "/about" }, { label: "Contact", path: "/contact" }].map((t) => (
          <Link key={t.path} href={t.path}><span className={`nav-tab cursor-pointer ${t.label === "About" ? "nav-tab-mobile-hidden" : ""} ${loc === t.path ? "active" : ""}`}>{t.label}</span></Link>
        ))}
        <div className="w-px h-6 bg-black/8 mx-1" />
        <Link href="/contact"><button className="group flex items-center gap-2 px-4 py-1.5 rounded-full font-semibold text-sm text-white active:scale-[0.98]" style={{ backgroundColor: "#C8962E" }}>Book Now<span className="btn-icon-circle light"><ChefHat className="w-3.5 h-3.5 text-white" strokeWidth={1.5} /></span></button></Link>
      </div>
    </nav>
  );
}

function CtaButton({ href, bg, text, icon: Icon }: { href: string; bg: string; text: string; icon: LucideIcon }) {
  return (
    <Link href={href}>
      <button className="group flex items-center gap-3 px-6 py-3 rounded-full font-semibold text-white active:scale-[0.98] text-sm" style={{ backgroundColor: bg }}>
        <span>{text}</span><span className="btn-icon-circle light"><Icon className="w-3.5 h-3.5 text-white" strokeWidth={1.5} /></span>
      </button>
    </Link>
  );
}

export default function Packages() {
  return (
    <div className="min-h-screen bg-white">
      <NavBar />

      <section className="pt-36 pb-16 md:pt-44 md:pb-24 bg-[#FDFBF7] text-center">
        <div className="container">
          <div className="eyebrow bg-[#C8962E]/10 text-[#C8962E] mx-auto w-fit mb-6"><Sparkles className="w-3 h-3" strokeWidth={1.5} /> Transparent pricing</div>
          <h1 style={{ color: "#1A5632" }} className="mb-4">Clear numbers, zero surprises.</h1>
          <p className="text-[#6B5E4A] max-w-lg mx-auto leading-relaxed">Choose the package that fits your event. Custom proposals available for anything larger.</p>
        </div>
      </section>

      {/* ── Tiers — Double-bezel ── */}
      <RevealSection className="section-spacing bg-white">
        <div className="container">
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { name: "Essential Bar", guests: "50–100 guests", desc: "Intimate gatherings and small celebrations.", price: "$1,200", features: ["1 Professional Bartender", "Premium Bar Equipment", "Glassware & Garnishes", "Mixers & Ice", "Full Setup & Breakdown", "Alcohol Consultation", "Up to 4 hours"], icon: Wine },
              { name: "Premium Experience", guests: "100–250 guests", desc: "Our most requested — weddings and corporate events.", price: "$2,400", features: ["2 Professional Bartenders", "Premium Bar Equipment", "Glassware & Garnishes", "Mixers & Ice", "Full Setup & Breakdown", "Alcohol Consultation", "Delivery Coordination", "Custom Cocktail Menu", "Up to 6 hours"], icon: Sparkles, recommended: true },
              { name: "Grand Celebration", guests: "250+ guests", desc: "Full-scale bar management for galas and large events.", price: "Custom Quote", features: ["3+ Professional Bartenders", "Full Bar Management", "Premium Equipment & Setup", "Glassware & Garnishes", "Mixers & Ice", "Complete Setup & Breakdown", "Alcohol Strategy", "Delivery Coordination", "Custom Cocktail Menu", "On-Site Bar Manager", "Post-Event Summary", "Custom duration"], icon: Martini },
            ].map((pkg, i) => (
              <div key={i} className={`card-shell reveal-up ${pkg.recommended ? "md:-mt-4 md:-mb-4" : ""}`} style={{ transitionDelay: `${i * 120}ms` }}>
                <div className="card-core flex flex-col h-full" style={pkg.recommended ? { borderColor: "#C8962E" } : {}}>
                  {pkg.recommended && (
                    <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold mb-5" style={{ backgroundColor: "#C8962E", color: "#fff" }}>
                      <Sparkles className="w-3 h-3" strokeWidth={1.5} /> Most popular
                    </div>
                  )}
                  <div className="w-11 h-11 rounded-2xl flex items-center justify-center mb-4" style={{ backgroundColor: pkg.recommended ? "#C8962E" : "#1A5632" }}>
                    <pkg.icon className="w-5 h-5 text-white" strokeWidth={1.5} />
                  </div>
                  <h3 style={{ color: "#1A5632" }} className="mb-1">{pkg.name}</h3>
                  <p className="text-[#8B7355] text-sm mb-1">{pkg.guests}</p>
                  <p className="text-[#8B7355] text-sm mb-6">{pkg.desc}</p>
                  <div className="text-4xl font-bold mb-8" style={{ color: "#1A5632" }}>{pkg.price}</div>
                  <ul className="space-y-3 mb-8 flex-grow">
                    {pkg.features.map((f, j) => (
                      <li key={j} className="flex items-start gap-2.5 text-sm">
                        <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: "#2D8A4E" }} strokeWidth={1.5} />
                        <span className="text-[#6B5E4A]">{f}</span>
                      </li>
                    ))}
                  </ul>
                  <Link href="/contact">
                    <button className="w-full group flex items-center justify-center gap-3 rounded-full py-3 font-semibold text-sm active:scale-[0.98] text-white" style={{ backgroundColor: pkg.recommended ? "#C8962E" : "#1A5632" }}>
                      Get started
                      <span className="btn-icon-circle light"><BookOpen className="w-3.5 h-3.5 text-white" strokeWidth={1.5} /></span>
                    </button>
                  </Link>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-12 rounded-2xl p-6 text-center bg-[#FDFBF7] border border-[#E8DFD0]">
            <p className="text-[#6B5E4A] text-sm"><strong>Alcohol:</strong> Purchased separately from your supplier. We handle recommendations and delivery logistics — you pay the supplier directly, zero markup.</p>
          </div>
        </div>
      </RevealSection>

      {/* ── Add-ons ── */}
      <RevealSection className="section-spacing bg-[#FDFBF7]">
        <div className="container">
          <h2 className="text-center mb-12" style={{ color: "#1A5632" }}>Available add-ons</h2>
          <div className="grid md:grid-cols-2 gap-5 max-w-4xl mx-auto">
            {[
              { title: "Additional Bartender", desc: "Extra bartender for larger events or extended hours", price: "$300/hr" },
              { title: "Coffee Bar Add-on", desc: "Full espresso bar with barista for morning or late-night service. Minimum 50 people.", price: "Starting at $15/person" },
              { title: "Mocktail Station", desc: "Dedicated zero-proof cocktail station with premium ingredients", price: "Starting at $18/person" },
              { title: "Custom Cocktail Menu", desc: "Simple cocktail menu and frame included with all packages. [Click here] to see custom branded event options.", price: "Included" },
              { title: "Wine Tasting Experience", desc: "Upgrade your event experience — we bring the winery to you", price: "Starting at $20/person" },
              { title: "Premium Glassware Upgrade", desc: "Plasticware is included with all of our packages. Upgrade to glassware for an elevated experience.", price: "$7/person" },
              { title: "Branded Bar Setup", desc: "Custom signage and branded bar aesthetic", price: "Starting at $150" },
            ].map((a, i) => (
              <div key={i} className="card-shell reveal-up" style={{ transitionDelay: `${i * 60}ms` }}>
                <div className="card-core !p-5 !rounded-[calc(2rem-0.5rem)]">
                  <div className="flex justify-between items-start gap-4">
                    <div><h4 className="font-bold text-sm" style={{ color: "#1A5632" }}>{a.title}</h4><p className="text-[#6B5E4A] text-xs mt-1">{a.desc}</p></div>
                    <span className="font-bold text-sm flex-shrink-0" style={{ color: "#C8962E" }}>{a.price}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </RevealSection>

      {/* ── CTA ── */}
      <section className="py-24 text-center" style={{ backgroundColor: "#1A5632" }}>
        <div className="container">
          <h2 className="text-white mb-4" style={{ color: "#fff" }}>Not sure which fits?</h2>
          <p className="text-[#D8CFB8] max-w-md mx-auto mb-8 leading-relaxed">We will help you pick the right package. Detailed proposals within 24 hours.</p>
          <CtaButton href="/contact" bg="#C8962E" text="Request a custom quote" icon={BookOpen} />
        </div>
      </section>

      {/* ── Footer ── */}
      <footer style={{ backgroundColor: "#1E1810", color: "#FDFBF7" }} className="py-20">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
            <div><h4 className="font-bold mb-4 text-lg" style={{ fontFamily: "'Playfair Display', serif", color: "#F5D77A" }}>BevPro</h4><p className="text-[#B8A88A] text-sm">Premium beverage catering.<br />Atlanta, Georgia.</p><SocialLinks className="mt-5" /></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Services</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li>Alcohol Catering</li><li>Coffee Catering</li><li>Mocktail Packages</li><li>Wine Tasting</li><li>Mixology Classes</li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Links</h5><ul className="space-y-2.5 text-sm"><li><Link href="/packages"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Packages</span></Link></li><li><Link href="/about"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">About</span></Link></li><li><Link href="/contact"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Contact</span></Link></li><li><a href="https://www.groupon.com" target="_blank" rel="noopener noreferrer" className="text-[#B8A88A] hover:text-white transition-colors duration-500">Groupon</a></li><li><Link href="/terms"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Terms</span></Link></li><li><Link href="/privacy"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Privacy</span></Link></li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Contact</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li><a href="mailto:hello@mybevpro.com" className="hover:text-white transition-colors duration-500">hello@mybevpro.com</a></li><li><a href="tel:+16788881505" className="hover:text-white transition-colors duration-500">(678) 888-1505</a></li><li>Atlanta, GA</li></ul></div>
          </div>
          <div className="border-t border-white/10 pt-8 text-center text-xs text-[#6B5E4A]"><p>&copy; 2026 BevPro LLC. All rights reserved.</p></div>
        </div>
      </footer>
    </div>
  );
}
