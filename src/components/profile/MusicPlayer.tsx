import { Music } from "lucide-react";

interface MusicPlayerProps {
  url: string;
}

export function MusicPlayer({ url }: MusicPlayerProps) {
  // Basic URL validation
  const isSpotify = url.includes("spotify.com");
  const isYoutube = url.includes("youtube.com") || url.includes("youtu.be");

  if (!isSpotify && !isYoutube) {
    return null;
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <Music className="h-5 w-5" />
        <h3 className="font-semibold">Now Playing</h3>
      </div>
      <div className="w-full h-[80px] bg-muted rounded-md">
        <iframe
          src={url}
          width="100%"
          height="80"
          frameBorder="0"
          allowTransparency={true}
          allow="encrypted-media"
          className="rounded-md"
        />
      </div>
    </div>
  );
}