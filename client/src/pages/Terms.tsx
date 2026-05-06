import { Link, useLocation } from "wouter";
import { ChefHat, BookOpen, type LucideIcon } from "lucide-react";
import { useEffect, useRef } from "react";
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

export default function Terms() {
  return (
    <div className="min-h-screen bg-white">
      <NavBar />

      <section className="pt-36 pb-16 md:pt-44 md:pb-24 bg-[#FDFBF7] text-center">
        <div className="container">
          <h1 style={{ color: "#1A5632" }} className="mb-4">Terms &amp; Conditions</h1>
          <p className="text-[#6B5E4A] max-w-lg mx-auto leading-relaxed text-sm">Last updated: May 1, 2026</p>
        </div>
      </section>

      <RevealSection className="section-spacing bg-white">
        <div className="container max-w-3xl">
          <div className="prose prose-stone max-w-none text-[#6B5E4A] text-sm leading-relaxed space-y-8">
            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>1. Acceptance of Terms</h3>
              <p>By accessing or using BevPro LLC (&ldquo;BevPro,&rdquo; &ldquo;we,&rdquo; &ldquo;us,&rdquo; or &ldquo;our&rdquo;) services, including our website at mybevpro.com and any related mobile bar catering, coffee catering, mocktail packages, wine tasting experiences, mixology classes, and bartender training (collectively, the &ldquo;Services&rdquo;), you agree to be bound by these Terms and Conditions. If you do not agree, please do not use our Services.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>2. Services Description</h3>
              <p>BevPro provides mobile bar catering and beverage services in the Atlanta, Georgia metropolitan area. Our Services include but are not limited to: alcohol catering, coffee catering, mocktail packages, wine tasting experiences, hands-on mixology classes, and professional bartender training. All Services are provided on a dry-hire basis unless otherwise agreed in writing — meaning the client purchases alcohol separately from their preferred supplier, and BevPro provides professional staffing, equipment, setup, service, and breakdown.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>3. Booking &amp; Payment</h3>
              <p><strong>Deposits:</strong> A non-refundable deposit of 50% of the total service fee is required to secure your event date. The remaining balance is due 14 days prior to the event date.</p>
              <p className="mt-2"><strong>Cancellations:</strong> Cancellations made more than 30 days before the event date will receive a refund of any payments made beyond the non-refundable deposit. Cancellations within 14–30 days receive a 50% refund of payments beyond the deposit. Cancellations within 14 days are non-refundable.</p>
              <p className="mt-2"><strong>Rescheduling:</strong> Events may be rescheduled once at no additional charge if notice is given at least 21 days before the original date. Rescheduling within 21 days is subject to availability and a $200 administrative fee.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>4. Alcohol &amp; Liability</h3>
              <p><strong>Dry-Hire Model:</strong> Under our standard dry-hire arrangement, the client is responsible for purchasing all alcoholic beverages from their chosen supplier. BevPro provides recommendations on brands and quantities but does not sell, furnish, or supply alcohol directly.</p>
              <p className="mt-2"><strong>Compliance:</strong> The client is responsible for ensuring that the event venue permits alcohol service and that all applicable local, state, and federal laws are followed. BevPro bartenders reserve the right to refuse service to any guest who appears intoxicated or under the legal drinking age.</p>
              <p className="mt-2"><strong>Insurance:</strong> BevPro maintains general liability insurance. Certificates of insurance can be provided to venues upon request.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>5. Mixology Classes</h3>
              <p>Mixology classes are offered as private group workshops or public sessions. Participants must be 21 years of age or older to consume alcohol during classes. BevPro provides all tools, ingredients, and recipe materials. Class participants assume all responsibility for their own safety and consumption during the workshop. Groupon vouchers are subject to Groupon&rsquo;s separate terms and conditions in addition to these Terms.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>5b. Bartender Training Program</h3>
              <p>The Bartender Training Program is a 4-week professional course designed to prepare students for employment in the bar and hospitality industry. The program includes classroom instruction, hands-on practice, certification preparation, and a guaranteed work placement at a live festival event. Program tuition is $1,499. Students must be 21 years of age or older. Upon successful completion, BevPro guarantees placement at one festival event within 60 days of graduation. If a placement is not secured within that window, the student is entitled to a full refund of tuition. Students are responsible for their own transportation to and from the festival venue. Festival work is compensated at the prevailing event rate and is separate from program tuition.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>6. Client Responsibilities</h3>
              <p>The client agrees to: (a) provide accurate event details including guest count, venue address, and event duration; (b) ensure the venue has adequate space, power, and water access for bar setup; (c) secure any necessary permits or venue approvals for alcohol service; (d) communicate any changes to the event plan at least 7 days in advance.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>7. Limitation of Liability</h3>
              <p>To the fullest extent permitted by law, BevPro&rsquo;s liability for any claim arising from our Services is limited to the total fees paid by the client for the specific event in question. BevPro is not liable for indirect, consequential, or incidental damages, including but not limited to lost profits or reputational harm.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>8. Intellectual Property</h3>
              <p>All content on the BevPro website — including text, images, logos, cocktail recipes, and menu designs — is the property of BevPro LLC and protected by applicable copyright and trademark laws. Custom cocktail menus created for clients remain the intellectual property of BevPro unless otherwise agreed in writing.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>9. Changes to Terms</h3>
              <p>BevPro reserves the right to update these Terms at any time. Changes will be posted on this page with an updated effective date. Continued use of our Services after changes constitutes acceptance of the revised Terms.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>10. Governing Law</h3>
              <p>These Terms are governed by the laws of the State of Georgia, without regard to conflict of law principles. Any disputes shall be resolved in the state or federal courts located in Fulton County, Georgia.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>11. Contact</h3>
              <p>For questions about these Terms, contact us at:</p>
              <p className="mt-1">BevPro LLC<br />Atlanta, GA<br /><a href="mailto:hello@mybevpro.com" style={{ color: "#2D8A4E" }}>hello@mybevpro.com</a><br />(404) 555-1234</p>
            </div>
          </div>
        </div>
      </RevealSection>

      <footer style={{ backgroundColor: "#1E1810", color: "#FDFBF7" }} className="py-20">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
            <div><h4 className="font-bold mb-4 text-lg" style={{ fontFamily: "'Playfair Display', serif", color: "#F5D77A" }}>BevPro</h4><p className="text-[#B8A88A] text-sm">Premium beverage catering.<br />Atlanta, Georgia.</p><SocialLinks className="mt-5" /></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Services</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li>Alcohol Catering</li><li>Coffee Catering</li><li>Mocktail Packages</li><li>Wine Tasting</li><li>Mixology Classes</li><li>Bartender Training</li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Links</h5><ul className="space-y-2.5 text-sm"><li><Link href="/packages"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Packages</span></Link></li><li><Link href="/about"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">About</span></Link></li><li><Link href="/contact"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Contact</span></Link></li><li><a href="https://www.groupon.com" target="_blank" rel="noopener noreferrer" className="text-[#B8A88A] hover:text-white transition-colors duration-500">Groupon</a></li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Legal</h5><ul className="space-y-2.5 text-sm"><li><Link href="/terms"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Terms &amp; Conditions</span></Link></li><li><Link href="/privacy"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Privacy Policy</span></Link></li></ul></div>
          </div>
          <div className="border-t border-white/10 pt-8 text-center text-xs text-[#6B5E4A]"><p>&copy; 2026 BevPro LLC. All rights reserved.</p></div>
        </div>
      </footer>
    </div>
  );
}
