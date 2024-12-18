import { ProfileHeader } from "./ProfileHeader";
import { SocialLinks } from "./SocialLinks";

interface ProfileContentProps {
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
  fontFamily: string;
  fontColor: string;
}

export function ProfileContent({
  username,
  avatarUrl,
  mood,
  bio,
  socialLinks,
  fontFamily,
  fontColor,
}: ProfileContentProps) {
  return (
    <div style={{ fontFamily, color: fontColor }} className="space-y-4">
      <ProfileHeader username={username} avatarUrl={avatarUrl} mood={mood} />
      
      {socialLinks?.myspace && (
        <div className="text-sm">
          <span className="font-semibold">MySpace URL: </span>
          <a 
            href={socialLinks.myspace}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            {socialLinks.myspace}
          </a>
        </div>
      )}
      
      {socialLinks && Object.values(socialLinks).some(link => link) && (
        <SocialLinks links={socialLinks} />
      )}
    </div>
  );
}