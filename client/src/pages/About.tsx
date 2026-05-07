import { Button } from "@/components/ui/button";
import { Link, useLocation } from "wouter";
import { Shield, Zap, Users, Eye, MapPin, BookOpen, ChefHat, type LucideIcon } from "lucide-react";
import { useEffect, useRef } from "react";
import { IMG } from "@/lib/images";
import SocialLinks from "@/components/SocialLinks";

function useScrollReveal() {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      (entries) => { entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add("visible"); obs.unobserve(entry.target); } }); },
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
      <div className="flex items-center gap-1 bg-white/85 backdrop-blur-xl rounded-full px-1.5 py-1.5 border border-black/5 shadow-diffuse">
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

export default function About() {
  return (
    <div className="min-h-screen bg-white">
      <NavBar />

      <section className="pt-36 pb-16 md:pt-44 md:pb-24 text-center" style={{ backgroundColor: "#1A5632" }}>
        <div className="container">
          <div className="eyebrow bg-white/15 text-[#F5D77A] mx-auto w-fit mb-6"><MapPin className="w-3 h-3" strokeWidth={1.5} /> Atlanta, Georgia</div>
          <h1 className="text-white mb-4" style={{ color: "#fff" }}>Atlanta's top <span style={{ color: "#F5D77A" }}>beverage catering</span> company.</h1>
          <p className="text-[#D8CFB8] max-w-xl mx-auto leading-relaxed">From craft cocktails to artisanal coffee — we bring the bar to you with precision, warmth, and a standard that speaks for itself.</p>
        </div>
      </section>

      <RevealSection className="section-spacing bg-white">
        <div className="container max-w-4xl">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="reveal-up">
              <h2 style={{ color: "#1A5632" }} className="mb-6">Why we exist.</h2>
              <p className="text-[#6B5E4A] mb-5 leading-relaxed">Georgia deserved a beverage catering company that treats every event like it is the only one that matters. Too many services show up, pour, and disappear. We create experiences people remember.</p>
              <p className="text-[#6B5E4A] mb-5 leading-relaxed">Our model puts you in control of your alcohol budget while we handle expertise, logistics, and execution. No surprises. No stress. Just exceptional service from people who care.</p>
              <p className="text-[#6B5E4A] leading-relaxed">From weddings to corporate galas — we have served hundreds of events across Georgia and built relationships that last.</p>
            </div>
            <div className="reveal-up" style={{ transitionDelay: "150ms" }}>
              <div className="card-shell">
                <img src={IMG.aboutTeam} alt="Professional bartender preparing drinks" className="rounded-[calc(2rem-0.375rem)] w-full h-[380px] object-cover" loading="lazy" />
              </div>
            </div>
          </div>
        </div>
      </RevealSection>

      <RevealSection className="section-spacing bg-[#FDFBF7]">
        <div className="container">
          <h2 style={{ color: "#1A5632" }} className="text-center mb-14">What we stand on.</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { icon: Shield, title: "Accountability", desc: "We own every detail. Your event's outcome is our responsibility — period." },
              { icon: Zap, title: "Reliability", desc: "We show up. We set up. We deliver. Every single time, without exception." },
              { icon: Users, title: "Professionalism", desc: "Trained, certified, and experienced in high-stakes event settings." },
              { icon: Eye, title: "Transparency", desc: "No hidden costs. Clear communication from first conversation to final breakdown." },
            ].map((v, i) => (
              <div key={i} className="card-shell reveal-up" style={{ transitionDelay: `${i * 80}ms` }}>
                <div className="card-core text-center !p-6">
                  <div className="w-12 h-12 rounded-2xl flex items-center justify-center mx-auto mb-4" style={{ backgroundColor: "#1A5632" }}><v.icon className="w-5 h-5 text-white" strokeWidth={1.5} /></div>
                  <h4 className="font-bold mb-2 text-sm" style={{ color: "#1A5632" }}>{v.title}</h4>
                  <p className="text-[#6B5E4A] text-xs leading-relaxed">{v.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </RevealSection>

      <RevealSection className="section-spacing bg-white">
        <div className="container text-center">
          <div className="grid md:grid-cols-3 gap-6 max-w-3xl mx-auto mb-14">
            {[
              { stat: "500+", label: "Events served" },
              { stat: "95%", label: "Repeat client rate" },
              { stat: "10+", label: "Years in business" },
            ].map((p, i) => (
              <div key={i} className="card-shell reveal-up" style={{ transitionDelay: `${i * 100}ms` }}>
                <div className="card-core !p-8 !rounded-[calc(2rem-0.5rem)]">
                  <div className="text-4xl font-bold mb-2" style={{ fontFamily: "'Playfair Display', serif", color: "#C8962E" }}>{p.stat}</div>
                  <p className="text-[#6B5E4A] text-sm font-medium">{p.label}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="rounded-2xl p-10 bg-[#FDFBF7] border border-[#E8DFD0] max-w-2xl mx-auto">
            <p className="text-[#6B5E4A] text-base italic leading-relaxed">&ldquo;When your event has to be perfect, work with people who treat it like their own.&rdquo;</p>
            <p className="text-[#8B7355] mt-4 text-sm font-semibold">&mdash; The BevPro standard</p>
          </div>
        </div>
      </RevealSection>

      <section className="py-24 text-center" style={{ backgroundColor: "#C8962E" }}>
        <div className="container">
          <h2 className="text-white mb-4" style={{ color: "#fff" }}>Ready to work with us?</h2>
          <p className="text-[#FDFBF7] max-w-md mx-auto mb-8 leading-relaxed">Tell us about your event and we will build a proposal that fits.</p>
          <CtaButton href="/contact" bg="#1A5632" text="Get in touch" icon={BookOpen} />
        </div>
      </section>

      <footer style={{ backgroundColor: "#1E1810", color: "#FDFBF7" }} className="py-20">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
            <div><h4 className="font-bold mb-4 text-lg" style={{ fontFamily: "'Playfair Display', serif", color: "#F5D77A" }}>BevPro</h4><p className="text-[#B8A88A] text-sm">Premium beverage catering.<br />Atlanta, Georgia.</p><SocialLinks className="mt-5" /></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Services</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li>Alcohol Catering</li><li>Coffee Catering</li><li>Mocktail Packages</li><li>Wine Tasting</li><li>Mixology Classes</li><li>Bartender Training</li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Links</h5><ul className="space-y-2.5 text-sm"><li><Link href="/packages"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Packages</span></Link></li><li><Link href="/about"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">About</span></Link></li><li><Link href="/contact"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Contact</span></Link></li><li><a href="https://www.groupon.com" target="_blank" rel="noopener noreferrer" className="text-[#B8A88A] hover:text-white transition-colors duration-500">Groupon</a></li><li><Link href="/terms"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Terms</span></Link></li><li><Link href="/privacy"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Privacy</span></Link></li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Contact</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li><a href="mailto:hello@mybevpro.com" className="hover:text-white transition-colors duration-500">hello@mybevpro.com</a></li><li><a href="tel:+16788881505" className="hover:text-white transition-colors duration-500">(678) 888-1505</a></li><li>Atlanta, GA</li></ul></div>
          </div>
          <div className="border-t border-white/10 pt-8 text-center text-xs text-[#6B5E4A]"><p>&copy; 2026 BevPro LLC. All rights reserved.</p></div>
        </div>
      </footer>
    </div>
  );
}
