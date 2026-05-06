import { Button } from "@/components/ui/button";
import { Link, useLocation } from "wouter";
import {
  Briefcase,
  Music,
  Award,
  CheckCircle2,
  MapPin,
  Users,
  Star,
  Martini,
  ChefHat,
  BookOpen,
  Beer,
  Citrus,
  GlassWater,
  type LucideIcon,
} from "lucide-react";
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

function CtaButton({ href, bg, text, icon: Icon }: { href: string; bg: string; text: string; icon: LucideIcon }) {
  return (
    <Link href={href}>
      <button className="group flex items-center gap-3 px-6 py-3 rounded-full font-semibold text-white active:scale-[0.98] text-sm" style={{ backgroundColor: bg }}>
        <span>{text}</span><span className="btn-icon-circle light"><Icon className="w-3.5 h-3.5 text-white" strokeWidth={1.5} /></span>
      </button>
    </Link>
  );
}

export default function BartenderTraining() {
  return (
    <div className="min-h-screen bg-white">
      <NavBar />

      {/* ── Hero ── */}
      <section className="pt-36 pb-16 md:pt-44 md:pb-24 text-center relative overflow-hidden" style={{ backgroundColor: "#1E1810" }}>
        <div className="absolute inset-0 opacity-[0.04] pointer-events-none">
          <svg width="100%" height="100%">
            <defs>
              <pattern id="lines3" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">
                <line x1="0" y1="0" x2="0" y2="40" stroke="#F5D77A" strokeWidth="1" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#lines3)" />
          </svg>
        </div>
        <div className="container relative z-10">
          <div className="eyebrow bg-[#C8962E]/20 text-[#F5D77A] mx-auto w-fit mb-6">
            <Award className="w-3 h-3" strokeWidth={1.5} />
            Career Program
          </div>
          <h1 className="text-white mb-4" style={{ color: "#fff" }}>
            Bartender Training
            <br />
            <span style={{ color: "#F5D77A" }}>Get trained. Get hired. Work a festival.</span>
          </h1>
          <p className="text-[#B8A88A] max-w-xl mx-auto leading-relaxed">
            A 4-week professional program that prepares you for a career behind the bar. Graduate with industry skills, certification, and a guaranteed job placement at a live Atlanta festival.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
            <CtaButton href="/contact" bg="#C8962E" text="Apply now" icon={Briefcase} />
            <a href="#curriculum">
              <button className="group flex items-center gap-3 px-6 py-3 rounded-full font-semibold text-sm active:scale-[0.98] border" style={{ borderColor: "#F5D77A", color: "#F5D77A" }}>
                View curriculum
                <span className="btn-icon-circle light"><BookOpen className="w-3.5 h-3.5" strokeWidth={1.5} style={{ color: "#F5D77A" }} /></span>
              </button>
            </a>
          </div>
        </div>
      </section>

      {/* ── Program overview ── */}
      <RevealSection className="section-spacing bg-white">
        <div className="container">
          <div className="mb-14 text-center">
            <div className="eyebrow bg-[#1A5632]/10 text-[#1A5632] mx-auto w-fit mb-4">
              <MapPin className="w-3 h-3" strokeWidth={1.5} />
              Atlanta, Georgia
            </div>
            <h2 style={{ color: "#1A5632" }} className="mb-3">How it works.</h2>
            <p className="text-[#6B5E4A] max-w-xl mx-auto leading-relaxed">
              Four weeks from zero experience to working bartender. No prior knowledge needed — just commitment and drive.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { step: "01", icon: BookOpen, title: "Learn the craft", desc: "Master 40+ classic and modern cocktail recipes. Speed pouring, free-pour technique, and bar setup fundamentals.", color: "#1A5632" },
              { step: "02", icon: Users, title: "Service mastery", desc: "Customer service training, point-of-sale systems, bar flow management, and handling high-volume service.", color: "#2D8A4E" },
              { step: "03", icon: Award, title: "Get certified", desc: "Responsible alcohol service certification. Resume preparation and interview coaching for hospitality roles.", color: "#C8962E" },
              { step: "04", icon: Music, title: "Work a festival", desc: "Guaranteed placement at a live festival event. Real bar, real guests, real experience — with pay.", color: "#8B2252" },
            ].map((s, i) => (
              <div key={i} className="card-shell reveal-up" style={{ transitionDelay: `${i * 100}ms` }}>
                <div className="card-core text-center !p-6">
                  <div className="text-3xl font-bold mb-3" style={{ fontFamily: "'Playfair Display', serif", color: s.color }}>{s.step}</div>
                  <div className="w-11 h-11 rounded-2xl flex items-center justify-center mx-auto mb-4" style={{ backgroundColor: s.color }}>
                    <s.icon className="w-5 h-5 text-white" strokeWidth={1.5} />
                  </div>
                  <h4 className="font-bold text-sm mb-2" style={{ color: "#1A5632" }}>{s.title}</h4>
                  <p className="text-[#6B5E4A] text-xs leading-relaxed">{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </RevealSection>

      {/* ── Curriculum detail ── */}
      <div id="curriculum">
      <RevealSection className="section-spacing bg-[#FDFBF7]">
        <div className="container max-w-4xl">
          <h2 className="text-center mb-14" style={{ color: "#1A5632" }}>What you will learn.</h2>

          <div className="space-y-6">
            {[
              {
                icon: Martini,
                title: "Classic & Modern Cocktails",
                desc: "Master 40+ recipes including Old Fashioned, Margarita, Mojito, Espresso Martini, Negroni, and seasonal specials. Learn recipe structure so you can build drinks from memory — not cheat sheets.",
                color: "#1A5632",
              },
              {
                icon: Beer,
                title: "Speed & Accuracy",
                desc: "Pour counts, jigger technique, and free-pour precision. Build muscle memory for speed without sacrificing quality. Handle 4+ tickets at once during service simulations.",
                color: "#2D8A4E",
              },
              {
                icon: Citrus,
                title: "Garnish & Presentation",
                desc: "Knife skills for citrus, herbs, and specialty garnishes. Learn what makes a drink look as good as it tastes — from simple twists to dehydrated wheels.",
                color: "#C8962E",
              },
              {
                icon: GlassWater,
                title: "Bar Setup & Workflow",
                desc: "Mise en place for bartenders. Rail organization, ice management, glassware staging. Set up a bar that lets you move fast without crashing into yourself.",
                color: "#8B2252",
              },
              {
                icon: Users,
                title: "Service & Hospitality",
                desc: "Reading the room, managing tabs, handling difficult guests, and creating experiences people come back for. Technical skill gets you hired — service skill builds your reputation.",
                color: "#6F4E37",
              },
              {
                icon: Briefcase,
                title: "Industry Knowledge",
                desc: "Spirit categories, flavor profiling, bar economics, and career pathways. Understand the business so you know where you want to go — and how to get there.",
                color: "#1E1810",
              },
            ].map((item, i) => (
              <div key={i} className="reveal-up flex gap-6 p-6 rounded-2xl bg-white border border-[#E8DFD0]" style={{ transitionDelay: `${i * 80}ms` }}>
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0" style={{ backgroundColor: item.color }}>
                  <item.icon className="w-5 h-5 text-white" strokeWidth={1.5} />
                </div>
                <div>
                  <h4 className="font-bold text-sm mb-2" style={{ color: "#1A5632" }}>{item.title}</h4>
                  <p className="text-[#6B5E4A] text-sm leading-relaxed">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </RevealSection>
      </div>

      {/* ── Festival placement ── */}
      <section className="section-spacing relative overflow-hidden" style={{ backgroundColor: "#1A5632" }}>
      <RevealSection className="">
        <div className="absolute inset-0 opacity-[0.06] pointer-events-none">
          <svg width="100%" height="100%">
            <defs>
              <pattern id="dots3" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
                <circle cx="30" cy="30" r="2" fill="white" />
                <circle cx="45" cy="15" r="1.5" fill="white" />
                <circle cx="15" cy="45" r="1.5" fill="white" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#dots3)" />
          </svg>
        </div>

        <div className="container relative z-10">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div className="reveal-up">
              <div className="eyebrow bg-white/15 text-[#F5D77A] mb-6">
                <Music className="w-3 h-3" strokeWidth={1.5} />
                The payoff
              </div>
              <h2 className="text-white mb-4" style={{ color: "#fff" }}>
                Your first gig is <span style={{ color: "#F5D77A" }}>booked before you start.</span>
              </h2>
              <p className="text-[#D8CFB8] mb-8 leading-relaxed max-w-md">
                Graduate on Friday, work a festival on Saturday. Our placement guarantee means you walk out of the program with real bar experience on your resume — and a paycheck.
              </p>

              <div className="space-y-4 mb-8">
                {[
                  "Placement at an Atlanta-area festival within 60 days of graduation",
                  "Paid work — festival rates, not training wages",
                  "Supervised by experienced BevPro bartenders on-site",
                  "Multiple festival partners — music, food, arts, and cultural events",
                  "Full refund if placement is not secured within 60 days",
                ].map((item, i) => (
                  <div key={i} className="flex items-start gap-3 text-sm">
                    <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: "#F5D77A" }} strokeWidth={1.5} />
                    <span className="text-[#D8CFB8]">{item}</span>
                  </div>
                ))}
              </div>

              <CtaButton href="/contact" bg="#C8962E" text="Reserve your spot" icon={Music} />
            </div>

            <div className="reveal-up" style={{ transitionDelay: "200ms" }}>
              <div className="card-shell">
                <div className="card-core !p-8 text-center">
                  <Music className="w-12 h-12 mx-auto mb-4" style={{ color: "#F5D77A" }} strokeWidth={1.5} />
                  <h3 className="text-2xl font-bold mb-3" style={{ color: "#1A5632" }}>Guaranteed placement</h3>
                  <p className="text-[#6B5E4A] text-sm mb-6 leading-relaxed">
                    We partner with festivals and event companies across Atlanta to ensure every graduate gets real-world bar experience. Your placement is part of the program — not an optional extra.
                  </p>
                  <div className="grid grid-cols-2 gap-4 text-center">
                    {[
                      { stat: "100%", label: "Placement rate" },
                      { stat: "60d", label: "Max wait time" },
                      { stat: "$18–25", label: "Festival hourly" },
                      { stat: "3+", label: "Festival partners" },
                    ].map((s, i) => (
                      <div key={i} className="rounded-xl p-3" style={{ backgroundColor: "#F5F0E8" }}>
                        <div className="text-lg font-bold" style={{ color: "#1A5632" }}>{s.stat}</div>
                        <div className="text-[10px] uppercase tracking-wider text-[#8B7355] mt-0.5">{s.label}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </RevealSection>
      </section>

      {/* ── Testimonials ── */}
      <RevealSection className="section-spacing bg-white">
        <div className="container">
          <div className="mb-14 text-center">
            <div className="eyebrow bg-[#C8962E]/10 text-[#C8962E] mx-auto w-fit mb-4">
              <Star className="w-3 h-3" strokeWidth={1.5} />
              Graduate stories
            </div>
            <h2 style={{ color: "#1A5632" }} className="mb-3">Where our graduates work.</h2>
          </div>

          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {[
              {
                quote: "I went from zero experience to working Shaky Knees in four weeks. The speed drills alone were worth the tuition. Now I pick up shifts at three bars in Midtown.",
                author: "Jordan Ellis",
                role: "Graduate, Spring 2026 — Bartender at Rowdy Tiger",
              },
              {
                quote: "The placement guarantee is real. They had me booked at a music festival before I even finished week three. Walking into that first shift with real training behind me changed everything.",
                author: "Taylor Nguyen",
                role: "Graduate, Winter 2026 — Events bartender",
              },
              {
                quote: "I'd served tables before but never touched a bar. BevPro's program gave me the confidence to walk into any bar and get to work. The certification and resume coaching sealed the deal.",
                author: "Marcus Webb",
                role: "Graduate, Fall 2025 — Ticonderoga Club",
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
                    <div className="w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold" style={{ backgroundColor: "#1A5632", color: "#FDFBF7" }}>
                      {t.author.charAt(0)}
                    </div>
                    <div>
                      <p className="text-sm font-semibold" style={{ color: "#1A5632" }}>{t.author}</p>
                      <p className="text-xs text-[#8B7355]">{t.role}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </RevealSection>

      {/* ── Pricing ── */}
      <RevealSection className="section-spacing bg-[#FDFBF7]">
        <div className="container max-w-lg text-center">
          <div className="card-shell reveal-up">
            <div className="card-core !p-10">
              <Award className="w-12 h-12 mx-auto mb-4" style={{ color: "#C8962E" }} strokeWidth={1.5} />
              <h2 className="mb-2" style={{ color: "#1A5632" }}>Program tuition</h2>
              <div className="text-5xl font-bold mb-4" style={{ fontFamily: "'Playfair Display', serif", color: "#1A5632" }}>$1,499</div>
              <p className="text-[#6B5E4A] text-sm mb-6 leading-relaxed">4 weeks · Includes all materials · Certification included · Guaranteed placement</p>
              <hr className="border-[#E8DFD0] mb-6" />
              <ul className="space-y-3 text-left text-sm mb-8">
                {[
                  "40+ hours of hands-on instruction",
                  "All spirits, ingredients, and tools provided",
                  "Responsible alcohol service certification",
                  "Resume prep and interview coaching",
                  "Guaranteed festival placement within 60 days",
                  "Full refund if placement is not secured",
                  "Payment plans available",
                ].map((f, i) => (
                  <li key={i} className="flex items-start gap-2.5">
                    <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: "#2D8A4E" }} strokeWidth={1.5} />
                    <span className="text-[#6B5E4A]">{f}</span>
                  </li>
                ))}
              </ul>
              <CtaButton href="/contact" bg="#C8962E" text="Apply for next cohort" icon={Briefcase} />
              <p className="text-xs text-[#8B7355] mt-4">Next cohort starts June 2026. Limited to 12 students per session.</p>
            </div>
          </div>
        </div>
      </RevealSection>

      {/* ── FAQ ── */}
      <RevealSection className="section-spacing bg-white">
        <div className="container max-w-3xl">
          <h2 className="text-center mb-12" style={{ color: "#1A5632" }}>Common questions.</h2>
          <div className="space-y-6">
            {[
              {
                q: "Do I need any experience to enroll?",
                a: "None. The program is designed for complete beginners. If you have never touched a shaker, you are our ideal student. The only requirements are being 21+, motivated, and ready to work.",
              },
              {
                q: "How does the job placement guarantee work?",
                a: "Upon successful completion of all 4 weeks, we guarantee placement at a festival event within 60 days. If for any reason we cannot place you, you receive a full refund of your tuition. This is not a job interview — the job is part of the program.",
              },
              {
                q: "What kind of festivals do graduates work at?",
                a: "We partner with music festivals, food and wine festivals, arts and cultural events, and large-scale private events across the Atlanta metro area. Recent graduates have worked at Shaky Knees, Atlanta Food & Wine Festival, and regional music events.",
              },
              {
                q: "Is the festival work paid?",
                a: "Yes. Festival work is compensated at prevailing event rates ($18–$25/hr), paid by the event organizer, not deducted from your tuition. The festival placement is real work — you earn while you build your resume.",
              },
              {
                q: "What is the schedule like?",
                a: "The 4-week program runs Monday through Friday, 9 AM to 1 PM. This leaves afternoons and weekends free. Some flexibility is available — contact us to discuss your situation.",
              },
              {
                q: "Do you offer payment plans?",
                a: "Yes. We offer a 50/50 split: half at enrollment, half at week 2. Other arrangements available on request. We want the program to be accessible — reach out and we will find a plan that works.",
              },
              {
                q: "What certification do I receive?",
                a: "You receive a responsible alcohol service certification recognized by Georgia hospitality employers, plus a BevPro Certificate of Completion. We also provide a reference letter and verified skills checklist for your job applications.",
              },
              {
                q: "Can I work as a bartender anywhere after this program?",
                a: "Yes. The skills transfer to any bar environment — restaurants, hotels, nightclubs, event venues, catering companies. Our graduates work across the industry, and the festival experience gives you a real-world credential from day one.",
              },
            ].map((faq, i) => (
              <div key={i} className="reveal-up" style={{ transitionDelay: `${i * 60}ms` }}>
                <h4 className="font-bold text-base mb-2" style={{ color: "#1A5632", fontFamily: "'Plus Jakarta Sans', sans-serif" }}>{faq.q}</h4>
                <p className="text-[#6B5E4A] text-sm leading-relaxed">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </RevealSection>

      {/* ── CTA ── */}
      <section className="py-24 text-center" style={{ backgroundColor: "#C8962E" }}>
        <div className="container">
          <h2 className="text-white mb-4" style={{ color: "#fff" }}>Ready to start your career?</h2>
          <p className="text-[#FDFBF7] max-w-md mx-auto mb-8 leading-relaxed">
            Next cohort starts June 2026. 12 spots. First come, first served.
          </p>
          <CtaButton href="/contact" bg="#1A5632" text="Apply now — spots fill fast" icon={Briefcase} />
        </div>
      </section>

      {/* ── Footer ── */}
      <footer style={{ backgroundColor: "#1E1810", color: "#FDFBF7" }} className="py-20">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
            <div><h4 className="font-bold mb-4 text-lg" style={{ fontFamily: "'Playfair Display', serif", color: "#F5D77A" }}>BevPro</h4><p className="text-[#B8A88A] text-sm">Premium beverage catering.<br />Atlanta, Georgia.</p><SocialLinks className="mt-5" /></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Services</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li>Alcohol Catering</li><li>Coffee Catering</li><li>Mocktail Packages</li><li>Wine Tasting</li><li>Mixology Classes</li><li>Bartender Training</li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Links</h5><ul className="space-y-2.5 text-sm"><li><Link href="/packages"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Packages</span></Link></li><li><Link href="/about"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">About</span></Link></li><li><Link href="/contact"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Contact</span></Link></li><li><Link href="/bartender-training"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Bartender Training</span></Link></li><li><a href="https://www.groupon.com" target="_blank" rel="noopener noreferrer" className="text-[#B8A88A] hover:text-white transition-colors duration-500">Groupon</a></li><li><Link href="/terms"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Terms</span></Link></li><li><Link href="/privacy"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Privacy</span></Link></li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Contact</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li><a href="mailto:hello@mybevpro.com" className="hover:text-white transition-colors duration-500">hello@mybevpro.com</a></li><li><a href="tel:+14045551234" className="hover:text-white transition-colors duration-500">(404) 555-1234</a></li><li>Atlanta, GA</li></ul></div>
          </div>
          <div className="border-t border-white/10 pt-8 text-center text-xs text-[#6B5E4A]"><p>&copy; 2026 BevPro LLC. All rights reserved.</p></div>
        </div>
      </footer>
    </div>
  );
}
