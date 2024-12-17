import { Twitter, Instagram, Github } from "lucide-react";

interface SocialLinksProps {
  links: {
    twitter?: string;
    instagram?: string;
    github?: string;
  };
}

export function SocialLinks({ links }: SocialLinksProps) {
  return (
    <div className="flex gap-4">
      {links.twitter && (
        <a href={links.twitter} target="_blank" rel="noopener noreferrer">
          <Twitter className="h-6 w-6 hover:text-blue-400 transition-colors" />
        </a>
      )}
      {links.instagram && (
        <a href={links.instagram} target="_blank" rel="noopener noreferrer">
          <Instagram className="h-6 w-6 hover:text-pink-500 transition-colors" />
        </a>
      )}
      {links.github && (
        <a href={links.github} target="_blank" rel="noopener noreferrer">
          <Github className="h-6 w-6 hover:text-gray-600 transition-colors" />
        </a>
      )}
    </div>
  );
}