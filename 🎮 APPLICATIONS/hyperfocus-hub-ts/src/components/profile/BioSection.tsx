import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

interface BioSectionProps {
  bio: string;
  onChange: (value: string) => void;
}

export function BioSection({ bio, onChange }: BioSectionProps) {
  return (
    <div className="space-y-4">
      <Label>About Me</Label>
      <Textarea
        placeholder="Tell us about yourself..."
        value={bio}
        onChange={(e) => onChange(e.target.value)}
        className="min-h-[100px]"
      />
    </div>
  );
}