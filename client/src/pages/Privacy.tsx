import { Link, useLocation } from "wouter";
import { ChefHat } from "lucide-react";
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

export default function Privacy() {
  return (
    <div className="min-h-screen bg-white">
      <NavBar />

      <section className="pt-36 pb-16 md:pt-44 md:pb-24 bg-[#FDFBF7] text-center">
        <div className="container">
          <h1 style={{ color: "#1A5632" }} className="mb-4">Privacy Policy</h1>
          <p className="text-[#6B5E4A] max-w-lg mx-auto leading-relaxed text-sm">Last updated: May 1, 2026</p>
        </div>
      </section>

      <RevealSection className="section-spacing bg-white">
        <div className="container max-w-3xl">
          <div className="text-[#6B5E4A] text-sm leading-relaxed space-y-8">
            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>1. Introduction</h3>
              <p>BevPro LLC (&ldquo;BevPro,&rdquo; &ldquo;we,&rdquo; &ldquo;us,&rdquo; or &ldquo;our&rdquo;) respects your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website mybevpro.com or use our mobile bar catering, coffee catering, mocktail packages, wine tasting experiences, and mixology class and bartender training services (collectively, the &ldquo;Services&rdquo;).</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>2. Information We Collect</h3>
              <p><strong>Information you provide directly:</strong> When you submit a contact form, request a quote, or book our Services, we collect:</p>
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li>Name</li>
                <li>Email address</li>
                <li>Phone number</li>
                <li>Company name (if provided)</li>
                <li>Event details (date, type, guest count, venue location)</li>
                <li>Service preferences and notes</li>
              </ul>
              <p className="mt-3"><strong>Information collected automatically:</strong> When you visit our website, we may automatically collect certain information including your IP address, browser type, operating system, referring URLs, pages viewed, and the dates and times of your visits.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>3. How We Use Your Information</h3>
              <p>We use the information we collect to:</p>
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li>Respond to your inquiries and provide quotes for our Services</li>
                <li>Process and manage event bookings</li>
                <li>Communicate with you about your event, including confirmations and updates</li>
                <li>Send promotional communications about new services or Groupon offers (only with your consent)</li>
                <li>Improve our website and Services based on usage patterns</li>
                <li>Comply with legal obligations and enforce our Terms &amp; Conditions</li>
              </ul>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>4. How We Share Your Information</h3>
              <p>We do not sell, trade, or rent your personal information to third parties. We may share information:</p>
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li>With service providers who assist us in operating our website and business (e.g., email providers, hosting services), subject to confidentiality agreements</li>
                <li>With venues or suppliers as necessary to coordinate your event (with your prior approval)</li>
                <li>If required by law, court order, or governmental regulation</li>
                <li>To protect the rights, property, or safety of BevPro, our clients, or the public</li>
              </ul>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>5. Cookies &amp; Tracking Technologies</h3>
              <p>Our website may use cookies and similar tracking technologies to enhance your browsing experience, analyze website traffic, and understand where our visitors come from. You can control cookie settings through your browser. Disabling cookies may affect certain website functionality.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>6. Third-Party Links</h3>
              <p>Our website may contain links to third-party websites, including Groupon for promotional deals on our mixology classes. We are not responsible for the privacy practices or content of these external sites. We encourage you to review the privacy policies of any third-party services you use.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>7. Data Security</h3>
              <p>We implement reasonable administrative, technical, and physical security measures to protect your personal information. However, no method of transmission over the internet or electronic storage is 100% secure. We cannot guarantee absolute security of your data.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>8. Data Retention</h3>
              <p>We retain your personal information for as long as necessary to fulfill the purposes outlined in this Privacy Policy, unless a longer retention period is required by law. Event inquiry data is typically retained for 24 months after your last interaction with us.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>9. Your Rights</h3>
              <p>Depending on your location, you may have the right to:</p>
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li>Access the personal information we hold about you</li>
                <li>Request correction of inaccurate information</li>
                <li>Request deletion of your personal information</li>
                <li>Opt out of marketing communications at any time</li>
                <li>File a complaint with a relevant data protection authority</li>
              </ul>
              <p className="mt-3">To exercise these rights, contact us at <a href="mailto:hello@mybevpro.com" style={{ color: "#2D8A4E" }}>hello@mybevpro.com</a>.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>10. Children&rsquo;s Privacy</h3>
              <p>Our Services are not directed to individuals under the age of 21. We do not knowingly collect personal information from anyone under 21. Mixology class and bartender training participants must be 21 or older to consume alcohol during workshops; younger participants may attend non-consumption portions with guardian consent.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>11. Changes to This Policy</h3>
              <p>We may update this Privacy Policy from time to time. Changes will be posted on this page with an updated effective date. We encourage you to review this policy periodically to stay informed about how we protect your information.</p>
            </div>

            <div>
              <h3 className="font-bold text-base mb-3" style={{ color: "#1A5632" }}>12. Contact Us</h3>
              <p>If you have questions about this Privacy Policy or our data practices, contact us at:</p>
              <p className="mt-1">BevPro LLC<br />Atlanta, GA<br /><a href="mailto:hello@mybevpro.com" style={{ color: "#2D8A4E" }}>hello@mybevpro.com</a><br />(678) 888-1505</p>
            </div>
          </div>
        </div>
      </RevealSection>

      <footer style={{ backgroundColor: "#1E1810", color: "#FDFBF7" }} className="py-20">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
            <div><h4 className="font-bold mb-4 text-lg" style={{ fontFamily: "'Playfair Display', serif", color: "#F5D77A" }}>BevPro</h4><p className="text-[#B8A88A] text-sm">Premium beverage catering.<br />Atlanta, Georgia.</p><SocialLinks className="mt-5" /></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Services</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li>Alcohol Catering</li><li>Coffee Catering</li><li>Mocktail Packages</li><li>Wine Tasting</li><li>Mixology Classes</li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Links</h5><ul className="space-y-2.5 text-sm"><li><Link href="/packages"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Packages</span></Link></li><li><Link href="/about"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">About</span></Link></li><li><Link href="/contact"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Contact</span></Link></li><li><a href="https://www.groupon.com" target="_blank" rel="noopener noreferrer" className="text-[#B8A88A] hover:text-white transition-colors duration-500">Groupon</a></li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Legal</h5><ul className="space-y-2.5 text-sm"><li><Link href="/terms"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Terms &amp; Conditions</span></Link></li><li><Link href="/privacy"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Privacy Policy</span></Link></li></ul></div>
          </div>
          <div className="border-t border-white/10 pt-8 text-center text-xs text-[#6B5E4A]"><p>&copy; 2026 BevPro LLC. All rights reserved.</p></div>
        </div>
      </footer>
    </div>
  );
}
