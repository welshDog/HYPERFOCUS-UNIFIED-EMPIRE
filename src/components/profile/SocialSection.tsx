import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { LinkIcon } from "lucide-react";

interface SocialLinks {
  twitter?: string;
  instagram?: string;
  github?: string;
}

interface SocialSectionProps {
  socialLinks: SocialLinks;
  onChange: (platform: keyof SocialLinks, value: string) => void;
}

export function SocialSection({ socialLinks, onChange }: SocialSectionProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <LinkIcon className="h-5 w-5" />
        <h3 className="text-lg font-semibold">Social Links</h3>
      </div>
      <div className="grid gap-4">
        <div>
          <Label>Twitter</Label>
          <Input
            placeholder="Twitter profile URL"
            value={socialLinks.twitter || ''}
            onChange={(e) => onChange('twitter', e.target.value)}
          />
        </div>
        <div>
          <Label>Instagram</Label>
          <Input
            placeholder="Instagram profile URL"
            value={socialLinks.instagram || ''}
            onChange={(e) => onChange('instagram', e.target.value)}
          />
        </div>
        <div>
          <Label>GitHub</Label>
          <Input
            placeholder="GitHub profile URL"
            value={socialLinks.github || ''}
            onChange={(e) => onChange('github', e.target.value)}
          />
        </div>
      </div>
    </div>
  );
}