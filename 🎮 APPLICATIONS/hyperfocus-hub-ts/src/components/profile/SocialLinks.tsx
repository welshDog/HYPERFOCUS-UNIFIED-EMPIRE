import { Link } from "lucide-react";

interface SocialLinksProps {
  links: {
    myspace?: string;
  };
}

export function SocialLinks({ links }: SocialLinksProps) {
  return (
    <div className="flex gap-4">
      {links.myspace && (
        <a href={links.myspace} target="_blank" rel="noopener noreferrer">
          <Link className="h-5 w-5 hover:text-blue-600 transition-colors" />
        </a>
      )}
    </div>
  );
}