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
    myspace?: string;
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
      className="w-full min-h-[600px] rounded-lg shadow-lg overflow-hidden bg-[#D3E4FD]"
      style={backgroundStyle}
    >
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 p-6">
        <div className="md:col-span-8 space-y-4">
          <div className="bg-white/80 backdrop-blur-sm rounded-lg p-4 shadow">
            <ProfileContent
              username={username}
              avatarUrl={avatarUrl}
              mood={mood}
              bio={bio}
              socialLinks={socialLinks}
              fontFamily={fontFamily}
              fontColor={fontColor}
            />
          </div>
          
          <div className="bg-white/80 backdrop-blur-sm rounded-lg p-4 shadow">
            <h3 className="font-bold mb-2">Latest Blog Entry</h3>
            <div className="prose max-w-none">
              {bio || "No blog entries yet..."}
            </div>
          </div>
        </div>
        
        <div className="md:col-span-4 space-y-4">
          {playlistUrl && (
            <div className="bg-white/80 backdrop-blur-sm rounded-lg p-4 shadow">
              <h3 className="font-bold mb-2">🎵 Music</h3>
              <div className="aspect-video">
                <iframe
                  src={playlistUrl}
                  width="100%"
                  height="100%"
                  frameBorder="0"
                  allow="encrypted-media"
                  className="rounded"
                />
              </div>
            </div>
          )}
          
          <div className="bg-white/80 backdrop-blur-sm rounded-lg p-4 shadow">
            <h3 className="font-bold mb-2">Basic Info</h3>
            <div className="text-sm space-y-2">
              <p>Member since: {new Date().toLocaleDateString()}</p>
              <p>Last login: {new Date().toLocaleDateString()}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}