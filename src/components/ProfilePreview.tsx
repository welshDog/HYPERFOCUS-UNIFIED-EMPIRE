import { ProfileContent } from "./profile/ProfileContent";

interface ProfilePreviewProps {
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
  backgroundType: 'color' | 'image';
  backgroundValue: string;
  fontFamily: string;
  fontColor: string;
}

export function ProfilePreview({
  username,
  avatarUrl,
  mood,
  bio,
  socialLinks,
  playlistUrl,
  backgroundType,
  backgroundValue,
  fontFamily,
  fontColor,
}: ProfilePreviewProps) {
  const backgroundStyle = backgroundType === 'color'
    ? { backgroundColor: backgroundValue }
    : { backgroundImage: `url(${backgroundValue})`, backgroundSize: 'cover', backgroundPosition: 'center' };

  return (
    <div
      className="w-full h-full min-h-[400px] rounded-lg shadow-lg overflow-hidden"
      style={backgroundStyle}
    >
      <ProfileContent
        username={username}
        avatarUrl={avatarUrl}
        mood={mood}
        bio={bio}
        socialLinks={socialLinks}
        playlistUrl={playlistUrl}
        fontFamily={fontFamily}
        fontColor={fontColor}
      />
    </div>
  );
}