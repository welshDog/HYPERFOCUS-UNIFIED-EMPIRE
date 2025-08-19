import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Music } from "lucide-react";

interface MusicSectionProps {
  playlistUrl: string;
  onChange: (value: string) => void;
}

export function MusicSection({ playlistUrl, onChange }: MusicSectionProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Music className="h-5 w-5" />
        <Label>Music Playlist URL</Label>
      </div>
      <Input
        placeholder="Spotify or YouTube playlist URL"
        value={playlistUrl}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}