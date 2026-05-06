import { Button } from "@/components/ui/button";
import { Link, useLocation } from "wouter";
import { ChevronDown, MapPin, ChefHat, BookOpen, type LucideIcon } from "lucide-react";
import { useState, useEffect, useRef } from "react";
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
          <Link key={t.path} href={t.path}><span className={`nav-tab cursor-pointer ${loc === t.path ? "active" : ""}`}>{t.label}</span></Link>
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

export default function Contact() {
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null);
  const [formData, setFormData] = useState({ eventDate: "", eventType: "", guestCount: "", duration: "", location: "", service: "", notes: "", name: "", company: "", email: "", phone: "" });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Form:", formData);
    alert("Thanks for reaching out. We will respond within 1 business day.");
    setFormData({ eventDate: "", eventType: "", guestCount: "", duration: "", location: "", service: "", notes: "", name: "", company: "", email: "", phone: "" });
  };

  const faqs = [
    { question: "What areas do you serve?", answer: "BevPro is based in Atlanta and serves the entire metro area — Buckhead, Midtown, Decatur, Sandy Springs, Roswell, Alpharetta, Marietta, and surrounding communities. Contact us to confirm availability for your location." },
    { question: "What types of events do you cater?", answer: "Weddings, corporate events, private parties, galas, product launches, holiday parties, team building workshops, and more. Our mixology classes are especially popular for corporate team building and social gatherings." },
    { question: "How does alcohol purchasing work?", answer: "We use a dry-hire model: you purchase alcohol directly from your preferred supplier at retail price. We provide expert recommendations on brands and quantities. You pay the supplier — we handle the rest with zero alcohol markup." },
    { question: "Do you offer mixology classes for beginners?", answer: "Absolutely. Our classes are designed for every skill level — from complete beginners to cocktail enthusiasts. All tools, ingredients, and guidance are provided. Many students discover us through Groupon." },
    { question: "How far in advance should I book?", answer: "We recommend 4–6 weeks for events, 2–3 weeks for mixology classes, and 4 weeks minimum for bartender training. Rush requests are accommodated when possible — reach out and we will do our best." },
    { question: "Do you handle setup and breakdown?", answer: "Always. We arrive early, set up completely, execute during your event, and break down entirely. You handle nothing. This is included in every package." },
  ];

  return (
    <div className="min-h-screen bg-white">
      <NavBar />

      <section className="pt-36 pb-16 md:pt-44 md:pb-24 bg-[#FDFBF7] text-center">
        <div className="container">
          <div className="eyebrow bg-[#1A5632]/10 text-[#1A5632] mx-auto w-fit mb-6"><MapPin className="w-3 h-3" strokeWidth={1.5} /> Atlanta, GA</div>
          <h1 style={{ color: "#1A5632" }} className="mb-4">Let's make it happen.</h1>
          <p className="text-[#6B5E4A] max-w-md mx-auto leading-relaxed">Fill out the form and we will respond within 1 business day — with a detailed proposal, zero pressure.</p>
        </div>
      </section>

      <RevealSection className="section-spacing bg-white">
        <div className="container">
          <div className="grid md:grid-cols-3 gap-12">
            <div className="md:col-span-2 reveal-up">
              <form onSubmit={handleSubmit} className="bg-white rounded-3xl border border-[#E8DFD0] p-8 md:p-10">
                <h3 className="font-bold mb-6" style={{ color: "#1A5632", fontFamily: "'Playfair Display', serif" }}>Event details</h3>
                <div className="grid md:grid-cols-2 gap-5 mb-6">
                  <div><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Event Date *</label><input type="date" name="eventDate" value={formData.eventDate} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} /></div>
                  <div><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Service Interest *</label><select name="service" value={formData.service} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties}><option value="">Select a service</option><option value="alcohol">Alcohol Catering</option><option value="coffee">Coffee Catering</option><option value="mocktail">Mocktail Packages</option><option value="wine">Wine Tasting</option><option value="mixology">Mixology Class</option>
                    <option value="training">Bartender Training</option><option value="multiple">Multiple Services</option><option value="unsure">Not Sure Yet</option></select></div>
                </div>
                <div className="grid md:grid-cols-2 gap-5 mb-6">
                  <div><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Guest Count *</label><input type="number" name="guestCount" value={formData.guestCount} onChange={handleInputChange} required placeholder="e.g., 150" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} /></div>
                  <div><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Duration (hours) *</label><input type="number" name="duration" value={formData.duration} onChange={handleInputChange} required placeholder="e.g., 4" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} /></div>
                </div>
                <div className="grid md:grid-cols-2 gap-5 mb-6">
                  <div><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Event Type *</label><select name="eventType" value={formData.eventType} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties}><option value="">Select type</option><option value="wedding">Wedding</option><option value="corporate">Corporate Event</option><option value="party">Private Party</option><option value="gala">Gala / Fundraiser</option><option value="holiday">Holiday Party</option><option value="teambuilding">Team Building</option><option value="other">Other</option></select></div>
                  <div><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Venue / Location *</label><input type="text" name="location" value={formData.location} onChange={handleInputChange} required placeholder="e.g., Buckhead, Atlanta" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} /></div>
                </div>
                <div className="mb-6"><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Additional Notes</label><textarea name="notes" value={formData.notes} onChange={handleInputChange} placeholder="Tell us about your event, preferences, or special requests..." rows={4} className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} /></div>
                <hr className="my-8 border-[#E8DFD0]" />
                <h3 className="font-bold mb-6" style={{ color: "#1A5632", fontFamily: "'Playfair Display', serif" }}>Your information</h3>
                <div className="grid md:grid-cols-2 gap-5 mb-6">
                  <div><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Name *</label><input type="text" name="name" value={formData.name} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} /></div>
                  <div><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Company</label><input type="text" name="company" value={formData.company} onChange={handleInputChange} className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} /></div>
                </div>
                <div className="grid md:grid-cols-2 gap-5 mb-8">
                  <div><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Email *</label><input type="email" name="email" value={formData.email} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} /></div>
                  <div><label className="block text-[#1E1810] font-semibold text-sm mb-1.5">Phone *</label><input type="tel" name="phone" value={formData.phone} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl focus:outline-none focus:ring-2 text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} /></div>
                </div>
                <button type="submit" className="w-full group flex items-center justify-center gap-3 rounded-full py-4 font-bold text-base active:scale-[0.98] text-white" style={{ backgroundColor: "#1A5632" }}>
                  Send inquiry
                  <span className="btn-icon-circle light"><BookOpen className="w-3.5 h-3.5 text-white" strokeWidth={1.5} /></span>
                </button>
              </form>
            </div>
            <div className="reveal-up" style={{ transitionDelay: "200ms" }}>
              <div className="rounded-3xl p-8 mb-6 bg-[#FDFBF7] border border-[#E8DFD0]">
                <h4 className="font-bold mb-5" style={{ color: "#1A5632" }}>Direct contact</h4>
                <div className="space-y-5 text-sm">
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">Email</p><a href="mailto:hello@mybevpro.com" style={{ color: "#2D8A4E" }} className="hover:underline">hello@mybevpro.com</a></div>
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">Phone</p><a href="tel:+14045551234" style={{ color: "#2D8A4E" }} className="hover:underline">(404) 555-1234</a></div>
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">Location</p><p className="text-[#6B5E4A]">Atlanta, GA</p></div>
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">Hours</p><p className="text-[#6B5E4A]">Mon–Fri, 9 AM – 6 PM EST</p></div>
                </div>
              </div>
              <div className="rounded-3xl p-6 bg-white border border-[#E8DFD0] space-y-4">
                {["Your information is never shared.", "We respond within 1 business day.", "Get a proposal with zero obligation."].map((t, i) => (
                  <div key={i} className="flex items-start gap-3 text-sm"><span className="font-bold flex-shrink-0" style={{ color: "#2D8A4E" }}>✓</span><p className="text-[#6B5E4A]">{t}</p></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </RevealSection>

      <RevealSection className="section-spacing bg-[#FDFBF7]">
        <div className="container max-w-3xl">
          <h2 className="text-center mb-12" style={{ color: "#1A5632" }}>Common questions</h2>
          <div className="space-y-3">
            {faqs.map((faq, i) => (
              <div key={i} className="bg-white rounded-2xl border border-[#E8DFD0] overflow-hidden">
                <button onClick={() => setExpandedFaq(expandedFaq === i ? null : i)} className="w-full flex items-center justify-between p-5 text-left hover:bg-[#FDFBF7] transition-colors duration-300">
                  <h4 className="font-semibold text-sm pr-4" style={{ color: "#1A5632" }}>{faq.question}</h4>
                  <ChevronDown className={`w-4 h-4 flex-shrink-0 transition-transform duration-500 ease-[cubic-bezier(0.32,0.72,0,1)] ${expandedFaq === i ? "rotate-180" : ""}`} style={{ color: "#C8962E" }} strokeWidth={1.5} />
                </button>
                {expandedFaq === i && (
                  <div className="px-5 pb-5 border-t border-[#E8DFD0]"><p className="text-[#6B5E4A] text-sm pt-4 leading-relaxed">{faq.answer}</p></div>
                )}
              </div>
            ))}
          </div>
        </div>
      </RevealSection>

      <footer style={{ backgroundColor: "#1E1810", color: "#FDFBF7" }} className="py-20">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
            <div><h4 className="font-bold mb-4 text-lg" style={{ fontFamily: "'Playfair Display', serif", color: "#F5D77A" }}>BevPro</h4><p className="text-[#B8A88A] text-sm">Premium beverage catering.<br />Atlanta, Georgia.</p><SocialLinks className="mt-5" /></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Services</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li>Alcohol Catering</li><li>Coffee Catering</li><li>Mocktail Packages</li><li>Wine Tasting</li><li>Mixology Classes</li><li>Bartender Training</li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Links</h5><ul className="space-y-2.5 text-sm"><li><Link href="/packages"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Packages</span></Link></li><li><Link href="/about"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">About</span></Link></li><li><Link href="/contact"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Contact</span></Link></li><li><a href="https://www.groupon.com" target="_blank" rel="noopener noreferrer" className="text-[#B8A88A] hover:text-white transition-colors duration-500">Groupon</a></li><li><Link href="/terms"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Terms</span></Link></li><li><Link href="/privacy"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Privacy</span></Link></li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Contact</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li><a href="mailto:hello@mybevpro.com" className="hover:text-white transition-colors duration-500">hello@mybevpro.com</a></li><li><a href="tel:+14045551234" className="hover:text-white transition-colors duration-500">(404) 555-1234</a></li><li>Atlanta, GA</li></ul></div>
          </div>
          <div className="border-t border-white/10 pt-8 text-center text-xs text-[#6B5E4A]"><p>&copy; 2026 BevPro LLC. All rights reserved.</p></div>
        </div>
      </footer>
    </div>
  );
}
