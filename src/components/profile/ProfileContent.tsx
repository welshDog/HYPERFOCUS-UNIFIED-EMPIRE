import { ProfileHeader } from "./ProfileHeader";
import { SocialLinks } from "./SocialLinks";
import { MusicPlayer } from "./MusicPlayer";

interface ProfileContentProps {
  username: string;
  avatarUrl?: string;
  mood?: string;
  bio?: string;
  socialLinks?: {
    twitter?: string;
    instagram?: string;
    github?: string;
  };
  playlistUrl?: string;
  fontFamily: string;
  fontColor: string;
}

export function ProfileContent({
  username,
  avatarUrl,
  mood,
  bio,
  socialLinks,
  playlistUrl,
  fontFamily,
  fontColor,
}: ProfileContentProps) {
  return (
    <div style={{ fontFamily, color: fontColor }} className="space-y-6 p-6">
      <ProfileHeader username={username} avatarUrl={avatarUrl} mood={mood} />
      
      {bio && <p className="text-lg">{bio}</p>}
      
      {socialLinks && Object.values(socialLinks).some(link => link) && (
        <SocialLinks links={socialLinks} />
      )}
      
      {playlistUrl && <MusicPlayer url={playlistUrl} />}
    </div>
  );
}