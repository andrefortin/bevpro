import { Button } from "@/components/ui/button";
import { Link, useLocation } from "wouter";
import { Calendar, Clock, MapPin, Users, Wine, ChefHat, Sparkles, type LucideIcon } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import SocialLinks from "@/components/SocialLinks";
import {
  Form, FormControl, FormField, FormItem, FormLabel, FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";

// ──────────────── Zod Schema ────────────────
const intakeSchema = z.object({
  eventType: z.enum(["Wedding", "Anniversary", "Corporate", "Birthday", "Gala", "Holiday", "Other"], { message: "Event type is required" }),
  eventName: z.string().min(1, "Event name is required"),
  eventDate: z.string().min(1, "Event date is required"),
  eventLocation: z.string().min(1, "Event location is required"),
  startTime: z.string().min(1, "Start time is required"),
  endTime: z.string().min(1, "End time is required"),
  barHours: z.string().min(1, "Bar service hours is required"),
  guestCount: z.string().min(1, "Guest count is required"),
  permitRequired: z.enum(["yes", "no", "unsure"], { message: "Please select an option" }),
  serviceType: z.enum(["premium", "essential", "mixers", "wine", "mocktail", "coffee", "multiple", "unsure"], { message: "Service type is required" }),
  bartenders: z.string().optional(),
  barbacks: z.string().optional(),
  glasswareRental: z.enum(["yes", "no"], { message: "Please select an option" }),
  venueBar: z.enum(["yes", "no"], { message: "Please select an option" }),
  otherNotes: z.string().optional(),
  fullName: z.string().min(1, "Full name is required"),
  email: z.string().email("Valid email is required"),
  phone: z.string().min(1, "Phone number is required"),
  referralSource: z.enum(["returning", "referral", "search", "social", "groupon", "other"], { message: "Please select an option" }),
});

type IntakeForm = z.infer<typeof intakeSchema>;

// ──────────────── Helpers ────────────────
function useScrollReveal() {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      (entries) => { entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add("visible"); obs.unobserve(entry.target); } }); },
      { threshold: 0.12 },
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

function CtaButton({ href, bg, text, icon: Icon }: { href: string; bg: string; text: string; icon: LucideIcon }) {
  return (
    <Link href={href}>
      <button className="group flex items-center gap-3 px-6 py-3 rounded-full font-semibold text-white active:scale-[0.98] text-sm" style={{ backgroundColor: bg }}>
        <span>{text}</span><span className="btn-icon-circle light"><Icon className="w-3.5 h-3.5 text-white" strokeWidth={1.5} /></span>
      </button>
    </Link>
  );
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
        <Link href="/intake"><button className="group flex items-center gap-2 px-4 py-1.5 rounded-full font-semibold text-sm text-white active:scale-[0.98]" style={{ backgroundColor: "#C8962E" }}>Book Now<span className="btn-icon-circle light"><ChefHat className="w-3.5 h-3.5 text-white" strokeWidth={1.5} /></span></button></Link>
      </div>
    </nav>
  );
}

// ──────────────── Section Header ────────────────
function SectionHeader({ number, title, icon: Icon }: { number: number; title: string; icon: LucideIcon }) {
  return (
    <div className="flex items-center gap-3 mb-6">
      <span className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white" style={{ backgroundColor: "#1A5632" }}>{number}</span>
      <Icon className="w-4 h-4" style={{ color: "#C8962E" }} strokeWidth={1.5} />
      <h3 style={{ color: "#1A5632", fontFamily: "'Playfair Display', serif" }} className="text-lg">{title}</h3>
    </div>
  );
}

// ──────────────── MAIN PAGE ────────────────
export default function Intake() {
  const [submitted, setSubmitted] = useState(false);

  const form = useForm<IntakeForm>({
    resolver: zodResolver(intakeSchema),
    defaultValues: {
      eventType: undefined,
      eventName: "",
      eventDate: "",
      eventLocation: "",
      startTime: "",
      endTime: "",
      barHours: "",
      guestCount: "",
      permitRequired: undefined,
      serviceType: undefined,
      bartenders: "",
      barbacks: "",
      glasswareRental: undefined,
      venueBar: undefined,
      otherNotes: "",
      fullName: "",
      email: "",
      phone: "",
      referralSource: undefined,
    },
  });

  const onSubmit = (data: IntakeForm) => {
    console.log("Intake form submitted:", data);
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-white">
        <NavBar />
        <section className="pt-36 pb-16 md:pt-44 md:pb-24 bg-[#FDFBF7] text-center">
          <div className="container max-w-lg">
            <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6" style={{ backgroundColor: "#1A5632" }}>
              <Sparkles className="w-7 h-7 text-white" strokeWidth={1.5} />
            </div>
            <h1 style={{ color: "#1A5632", fontFamily: "'Playfair Display', serif" }} className="mb-4">We got it!</h1>
            <p className="text-[#6B5E4A] leading-relaxed mb-8">
              Thanks for telling us about your event. We'll put together a detailed proposal and get back to you within <strong>24 hours</strong> — no obligation, no pressure.
            </p>
            <CtaButton href="/" bg="#1A5632" text="Back to Home" icon={ChefHat} />
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <NavBar />

      {/* ── Header ── */}
      <section className="pt-36 pb-16 md:pt-44 md:pb-24 bg-[#FDFBF7] text-center">
        <div className="container">
          <div className="eyebrow bg-[#1A5632]/10 text-[#1A5632] mx-auto w-fit mb-6"><MapPin className="w-3 h-3" strokeWidth={1.5} /> Atlanta, GA</div>
          <h1 style={{ color: "#1A5632" }} className="mb-4">Plan your event with us.</h1>
          <p className="text-[#6B5E4A] max-w-lg mx-auto leading-relaxed">Tell us about your event and we'll build a custom proposal within 24 hours. Zero pressure — just a great bar experience.</p>
        </div>
      </section>

      {/* ── Form ── */}
      <RevealSection className="section-spacing bg-white">
        <div className="container">
          <div className="grid md:grid-cols-3 gap-12">
            <div className="md:col-span-2 reveal-up">
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="bg-white rounded-3xl border border-[#E8DFD0] p-8 md:p-10">

                  {/* ═══ SECTION 1: Event Logistics ═══ */}
                  <SectionHeader number={1} title="Event Logistics" icon={Calendar} />

                  <div className="space-y-6 mb-10">
                    {/* Q1: Event Type */}
                    <FormField control={form.control} name="eventType" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">What kind of event are you planning? <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties}>
                              <SelectValue placeholder="Select event type" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="Wedding">Wedding</SelectItem>
                            <SelectItem value="Anniversary">Anniversary</SelectItem>
                            <SelectItem value="Corporate">Corporate Event</SelectItem>
                            <SelectItem value="Birthday">Birthday Party</SelectItem>
                            <SelectItem value="Gala">Gala / Fundraiser</SelectItem>
                            <SelectItem value="Holiday">Holiday Party</SelectItem>
                            <SelectItem value="Other">Other</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )} />

                    {/* Q2: Event Name */}
                    <FormField control={form.control} name="eventName" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Please name your event <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <FormControl>
                          <Input {...field} placeholder="e.g., Schwarz / Malcom Wedding" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />

                    {/* Q3: Event Date */}
                    <FormField control={form.control} name="eventDate" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Event date <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <FormControl>
                          <Input {...field} type="date" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />

                    {/* Q4: Event Location */}
                    <FormField control={form.control} name="eventLocation" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Event location <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <FormControl>
                          <Input {...field} placeholder="e.g., 9 Oaks Farm, Monroe GA" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />

                    {/* Q5: Event Times — side by side */}
                    <div className="grid grid-cols-2 gap-5">
                      <FormField control={form.control} name="startTime" render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[#1E1810] font-semibold text-sm">Start time <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                          <FormControl>
                            <Input {...field} type="time" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )} />
                      <FormField control={form.control} name="endTime" render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[#1E1810] font-semibold text-sm">End time <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                          <FormControl>
                            <Input {...field} type="time" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )} />
                    </div>

                    {/* Q6: Bar Hours + Guest Count — side by side */}
                    <div className="grid grid-cols-2 gap-5">
                      <FormField control={form.control} name="barHours" render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[#1E1810] font-semibold text-sm">Total bar service hours <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                          <FormControl>
                            <Input {...field} type="number" placeholder="e.g., 5" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                          </FormControl>
                          <p className="text-[#8B7355] text-xs mt-1">Actual serving hours only — not including setup &amp; breakdown</p>
                          <FormMessage />
                        </FormItem>
                      )} />
                      <FormField control={form.control} name="guestCount" render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[#1E1810] font-semibold text-sm">Estimated guest count <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                          <FormControl>
                            <Input {...field} type="number" placeholder="e.g., 200" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )} />
                    </div>

                    {/* Q7: Permit */}
                    <FormField control={form.control} name="permitRequired" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Does your event require a local permit? <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <FormControl>
                          <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex gap-6 mt-1">
                            {[{ value: "yes", label: "Yes" }, { value: "no", label: "No" }, { value: "unsure", label: "Unsure" }].map((opt) => (
                              <div key={opt.value} className="flex items-center gap-2">
                                <RadioGroupItem value={opt.value} id={`permit-${opt.value}`} />
                                <Label htmlFor={`permit-${opt.value}`} className="text-[#6B5E4A] text-sm cursor-pointer">{opt.label}</Label>
                              </div>
                            ))}
                          </RadioGroup>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />
                  </div>

                  <hr className="my-8 border-[#E8DFD0]" />

                  {/* ═══ SECTION 2: Beverage & Service ═══ */}
                  <SectionHeader number={2} title="Beverage &amp; Service Details" icon={Wine} />

                  <div className="space-y-6 mb-10">
                    {/* Q8: Service Type */}
                    <FormField control={form.control} name="serviceType" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Type of beverage service needed? <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <p className="text-[#8B7355] text-xs">Non-alcoholic beverages included in all packages</p>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm mt-1" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties}>
                              <SelectValue placeholder="Select service type" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="premium">Premium Package (Signature Tier Liquor)</SelectItem>
                            <SelectItem value="essential">Essential Bar Package</SelectItem>
                            <SelectItem value="mixers">Mixers Package (BYO Alcohol)</SelectItem>
                            <SelectItem value="wine">Wine Tasting Experience</SelectItem>
                            <SelectItem value="mocktail">Mocktail Package</SelectItem>
                            <SelectItem value="coffee">Coffee Bar Package</SelectItem>
                            <SelectItem value="multiple">Multiple Services</SelectItem>
                            <SelectItem value="unsure">Not Sure Yet — Help Me Decide</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )} />

                    {/* Q9: Staffing */}
                    <div className="grid grid-cols-2 gap-5">
                      <FormField control={form.control} name="bartenders" render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[#1E1810] font-semibold text-sm">How many bartenders?</FormLabel>
                          <FormControl>
                            <Input {...field} type="number" min={0} placeholder="e.g., 2" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )} />
                      <FormField control={form.control} name="barbacks" render={({ field }) => (
                        <FormItem>
                          <FormLabel className="text-[#1E1810] font-semibold text-sm">Need barbacks?</FormLabel>
                          <FormControl>
                            <Input {...field} type="number" min={0} placeholder="e.g., 1" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )} />
                    </div>

                    {/* Q10: Ancillary — Glassware */}
                    <FormField control={form.control} name="glasswareRental" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Would you like to add glassware rental to your proposal? <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <p className="text-[#8B7355] text-xs">All packages include plasticware. Glassware rental available for an additional fee.</p>
                        <FormControl>
                          <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex gap-6 mt-1">
                            {[{ value: "yes", label: "Yes" }, { value: "no", label: "No" }].map((opt) => (
                              <div key={opt.value} className="flex items-center gap-2">
                                <RadioGroupItem value={opt.value} id={`glass-${opt.value}`} />
                                <Label htmlFor={`glass-${opt.value}`} className="text-[#6B5E4A] text-sm cursor-pointer">{opt.label}</Label>
                              </div>
                            ))}
                          </RadioGroup>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />

                    {/* Q10b: Venue Bar */}
                    <FormField control={form.control} name="venueBar" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Will we be using a venue-provided bar instead of our standard bar? <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <p className="text-[#8B7355] text-xs">Our standard bar is included with your package.</p>
                        <FormControl>
                          <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex gap-6 mt-1">
                            {[{ value: "yes", label: "Yes" }, { value: "no", label: "No" }].map((opt) => (
                              <div key={opt.value} className="flex items-center gap-2">
                                <RadioGroupItem value={opt.value} id={`venue-${opt.value}`} />
                                <Label htmlFor={`venue-${opt.value}`} className="text-[#6B5E4A] text-sm cursor-pointer">{opt.label}</Label>
                              </div>
                            ))}
                          </RadioGroup>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />

                    {/* Q11: Other Notes */}
                    <FormField control={form.control} name="otherNotes" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Other considerations we should note to curate your experience?</FormLabel>
                        <FormControl>
                          <Textarea {...field} placeholder="e.g., We'd like beer, wine, margaritas, old fashioned & espresso martinis as signature cocktails..." rows={4} className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />
                  </div>

                  <hr className="my-8 border-[#E8DFD0]" />

                  {/* ═══ SECTION 3: Contact Info ═══ */}
                  <SectionHeader number={3} title="Your Contact Information" icon={Users} />

                  <div className="space-y-6 mb-8">
                    {/* Q12: Full Name */}
                    <FormField control={form.control} name="fullName" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Full name <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <FormControl>
                          <Input {...field} placeholder="e.g., Jamie Schwarz" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />

                    {/* Q13: Email */}
                    <FormField control={form.control} name="email" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Email <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <FormControl>
                          <Input {...field} type="email" placeholder="e.g., jamie@example.com" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />

                    {/* Q14: Phone */}
                    <FormField control={form.control} name="phone" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">Phone number <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <FormControl>
                          <Input {...field} type="tel" placeholder="e.g., 985-778-3334" className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )} />

                    {/* Q15: Referral Source */}
                    <FormField control={form.control} name="referralSource" render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-[#1E1810] font-semibold text-sm">How did you hear about us? <span style={{ color: "#C8962E" }}>*</span></FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger className="w-full px-4 py-2.5 border border-[#E8DFD0] rounded-xl text-sm" style={{ "--tw-ring-color": "#2D8A4E" } as React.CSSProperties}>
                              <SelectValue placeholder="Select option" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="returning">Returning Client</SelectItem>
                            <SelectItem value="referral">Referral</SelectItem>
                            <SelectItem value="search">Online Search</SelectItem>
                            <SelectItem value="social">Social Media</SelectItem>
                            <SelectItem value="groupon">Groupon</SelectItem>
                            <SelectItem value="other">Other</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )} />
                  </div>

                  {/* ── Submit ── */}
                  <button type="submit" className="w-full group flex items-center justify-center gap-3 rounded-full py-4 font-bold text-base active:scale-[0.98] text-white" style={{ backgroundColor: "#1A5632" }}>
                    Submit intake form
                    <span className="btn-icon-circle light"><Sparkles className="w-3.5 h-3.5 text-white" strokeWidth={1.5} /></span>
                  </button>

                  <p className="text-[#8B7355] text-xs text-center mt-4">
                    Thank you for providing this information. We'll use these details to customize your proposal.
                  </p>
                </form>
              </Form>
            </div>

            {/* ── Sidebar ── */}
            <div className="reveal-up" style={{ transitionDelay: "200ms" }}>
              <div className="rounded-3xl p-8 mb-6 bg-[#FDFBF7] border border-[#E8DFD0]">
                <h4 className="font-bold mb-5" style={{ color: "#1A5632" }}>Why book with BevPro</h4>
                <div className="space-y-5 text-sm">
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">Dry-hire model</p><p className="text-[#6B5E4A]">You buy the alcohol at retail — zero markup. We handle everything else.</p></div>
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">Proposal in 24 hours</p><p className="text-[#6B5E4A]">Detailed pricing, no surprises, no obligation.</p></div>
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">TIPS-certified team</p><p className="text-[#6B5E4A]">Every bartender trained. Every event insured.</p></div>
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">Full setup &amp; breakdown</p><p className="text-[#6B5E4A]">We arrive early, leave clean. You focus on your guests.</p></div>
                </div>
              </div>

              <div className="rounded-3xl p-6 bg-white border border-[#E8DFD0] space-y-4">
                {["Your information is never shared.", "We respond within 1 business day.", "Get a proposal with zero obligation."].map((t, i) => (
                  <div key={i} className="flex items-start gap-3 text-sm"><span className="font-bold flex-shrink-0" style={{ color: "#2D8A4E" }}>✓</span><p className="text-[#6B5E4A]">{t}</p></div>
                ))}
              </div>

              <div className="rounded-3xl p-8 mt-6 bg-[#FDFBF7] border border-[#E8DFD0]">
                <h4 className="font-bold mb-4" style={{ color: "#1A5632" }}>Direct contact</h4>
                <div className="space-y-4 text-sm">
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">Email</p><a href="mailto:hello@mybevpro.com" style={{ color: "#2D8A4E" }} className="hover:underline">hello@mybevpro.com</a></div>
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">Phone</p><a href="tel:+14045551234" style={{ color: "#2D8A4E" }} className="hover:underline">(404) 555-1234</a></div>
                  <div><p className="text-[#1E1810] font-semibold mb-0.5">Location</p><p className="text-[#6B5E4A]">Atlanta, GA</p></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </RevealSection>

      {/* ── Footer ── */}
      <footer style={{ backgroundColor: "#1E1810", color: "#FDFBF7" }} className="py-20">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
            <div><h4 className="font-bold mb-4 text-lg" style={{ fontFamily: "'Playfair Display', serif", color: "#F5D77A" }}>BevPro</h4><p className="text-[#B8A88A] text-sm">Premium beverage catering.<br />Atlanta, Georgia.</p><SocialLinks className="mt-5" /></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Services</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li>Alcohol Catering</li><li>Coffee Catering</li><li>Mocktail Packages</li><li>Wine Tasting</li><li>Mixology Classes</li><li>Bartender Training</li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Links</h5><ul className="space-y-2.5 text-sm"><li><Link href="/packages"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Packages</span></Link></li><li><Link href="/about"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">About</span></Link></li><li><Link href="/contact"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Contact</span></Link></li><li><Link href="/intake"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Book an Event</span></Link></li><li><Link href="/terms"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Terms</span></Link></li><li><Link href="/privacy"><span className="text-[#B8A88A] hover:text-white cursor-pointer transition-colors duration-500">Privacy</span></Link></li></ul></div>
            <div><h5 className="font-semibold mb-4 text-xs uppercase tracking-widest text-[#8B7355]">Contact</h5><ul className="space-y-2.5 text-sm text-[#B8A88A]"><li><a href="mailto:hello@mybevpro.com" className="hover:text-white transition-colors duration-500">hello@mybevpro.com</a></li><li><a href="tel:+14045551234" className="hover:text-white transition-colors duration-500">(404) 555-1234</a></li><li>Atlanta, GA</li></ul></div>
          </div>
          <div className="border-t border-white/10 pt-8 text-center text-xs text-[#6B5E4A]"><p>&copy; 2026 BevPro LLC. All rights reserved.</p></div>
        </div>
      </footer>
    </div>
  );
}
