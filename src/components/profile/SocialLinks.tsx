import { Twitter, Instagram, Github, Link } from "lucide-react";

interface SocialLinksProps {
  links: {
    twitter?: string;
    instagram?: string;
    github?: string;
    myspace?: string;
  };
}

export function SocialLinks({ links }: SocialLinksProps) {
  return (
    <div className="flex gap-4">
      {links.twitter && (
        <a href={links.twitter} target="_blank" rel="noopener noreferrer">
          <Twitter className="h-5 w-5 hover:text-blue-400 transition-colors" />
        </a>
      )}
      {links.instagram && (
        <a href={links.instagram} target="_blank" rel="noopener noreferrer">
          <Instagram className="h-5 w-5 hover:text-pink-500 transition-colors" />
        </a>
      )}
      {links.github && (
        <a href={links.github} target="_blank" rel="noopener noreferrer">
          <Github className="h-5 w-5 hover:text-gray-600 transition-colors" />
        </a>
      )}
      {links.myspace && (
        <a href={links.myspace} target="_blank" rel="noopener noreferrer">
          <Link className="h-5 w-5 hover:text-blue-600 transition-colors" />
        </a>
      )}
    </div>
  );
}