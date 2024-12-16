import { useAuth } from "@/contexts/AuthContext";
import { Card } from "@/components/ui/card";
import { Music, Link as LinkIcon } from "lucide-react";

interface ProfilePreviewProps {
  profileData: {
    background_type: 'color' | 'image';
    background_value: string;
    font_family: string;
    font_color: string;
    bio: string;
    mood: string;
    playlist_url: string;
    social_links: {
      twitter?: string;
      instagram?: string;
      github?: string;
    };
  };
}

export function ProfilePreview({ profileData }: ProfilePreviewProps) {
  const { session } = useAuth();
  const username = session?.user.email?.split('@')[0] || 'User';

  const backgroundStyle = profileData.background_type === 'color'
    ? { backgroundColor: profileData.background_value }
    : { backgroundImage: `url(${profileData.background_value})`, backgroundSize: 'cover' };

  return (
    <Card className="w-full overflow-hidden animate-fade-in">
      <div
        className="p-6 min-h-[400px]"
        style={{
          ...backgroundStyle,
          fontFamily: profileData.font_family,
          color: profileData.font_color,
        }}
      >
        <div className="bg-white/80 backdrop-blur-sm p-4 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-4" style={{ color: profileData.font_color }}>
            {username}'s Profile
          </h2>

          {profileData.mood && (
            <p className="text-sm mb-4" style={{ color: profileData.font_color }}>
              Current Mood: {profileData.mood}
            </p>
          )}

          {profileData.bio && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2" style={{ color: profileData.font_color }}>
                About Me
              </h3>
              <p style={{ color: profileData.font_color }}>{profileData.bio}</p>
            </div>
          )}

          {profileData.playlist_url && (
            <div className="mb-6">
              <div className="flex items-center gap-2 mb-2">
                <Music className="h-4 w-4" style={{ color: profileData.font_color }} />
                <h3 className="text-lg font-semibold" style={{ color: profileData.font_color }}>
                  My Playlist
                </h3>
              </div>
              <a
                href={profileData.playlist_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline"
                style={{ color: profileData.font_color }}
              >
                Listen to my playlist
              </a>
            </div>
          )}

          {Object.keys(profileData.social_links).length > 0 && (
            <div className="mt-6">
              <div className="flex items-center gap-2 mb-2">
                <LinkIcon className="h-4 w-4" style={{ color: profileData.font_color }} />
                <h3 className="text-lg font-semibold" style={{ color: profileData.font_color }}>
                  Connect with me
                </h3>
              </div>
              <div className="flex gap-4">
                {Object.entries(profileData.social_links).map(([platform, url]) => (
                  url && (
                    <a
                      key={platform}
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:underline capitalize"
                      style={{ color: profileData.font_color }}
                    >
                      {platform}
                    </a>
                  )
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}