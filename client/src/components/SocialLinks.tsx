import { FaInstagram, FaTiktok, FaLinkedin, FaXTwitter } from "react-icons/fa6";

const LINKS = [
  {
    label: "Instagram",
    href: "https://www.instagram.com/mybevpro/",
    Icon: FaInstagram,
  },
  {
    label: "TikTok",
    href: "https://www.tiktok.com/@bevpro",
    Icon: FaTiktok,
  },
  {
    label: "LinkedIn",
    href: "#",
    Icon: FaLinkedin,
    placeholder: true,
  },
  {
    label: "X",
    href: "#",
    Icon: FaXTwitter,
    placeholder: true,
  },
];

export default function SocialLinks({ className = "" }: { className?: string }) {
  return (
    <div className={`flex items-center gap-3 ${className}`}>
      {LINKS.map(({ label, href, Icon, placeholder }) => (
        <a
          key={label}
          href={href}
          target={placeholder ? undefined : "_blank"}
          rel={placeholder ? undefined : "noopener noreferrer"}
          aria-label={`BevPro on ${label}${placeholder ? " — coming soon" : ""}`}
          title={`BevPro on ${label}${placeholder ? " — coming soon" : ""}`}
          className={`group relative flex items-center justify-center w-9 h-9 text-[#8B7355] hover:text-[#C8962E] transition-all duration-500 ease-[cubic-bezier(0.32,0.72,0,1)] ${placeholder ? "opacity-50" : ""}`}
        >
          <Icon className="w-[18px] h-[18px] transition-transform duration-500 ease-[cubic-bezier(0.32,0.72,0,1)] group-hover:scale-110 group-active:scale-95" />
        </a>
      ))}
    </div>
  );
}
