import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { LinkIcon } from "lucide-react";

interface SocialLinks {
  myspace?: string;
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
          <Label>MySpace</Label>
          <Input
            placeholder="MySpace profile URL"
            value={socialLinks.myspace || ''}
            onChange={(e) => onChange('myspace', e.target.value)}
          />
        </div>
      </div>
    </div>
  );
}