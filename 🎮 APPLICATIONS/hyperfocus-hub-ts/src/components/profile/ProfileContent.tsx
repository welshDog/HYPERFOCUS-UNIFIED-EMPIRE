import { ProfileHeader } from "./ProfileHeader";
import { SocialLinks } from "./SocialLinks";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";

interface ProfileContentProps {
  username: string;
  avatarUrl?: string;
  mood?: string;
  bio?: string;
  summary?: string;
  interests?: string[];
  accomplishments?: string[];
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
  summary,
  interests = [],
  accomplishments = [],
  socialLinks,
  fontFamily,
  fontColor,
}: ProfileContentProps) {
  return (
    <div style={{ fontFamily, color: fontColor }} className="space-y-6">
      <ProfileHeader username={username} avatarUrl={avatarUrl} mood={mood} />
      
      {summary && (
        <Card className="p-4">
          <h3 className="font-semibold mb-2">Summary</h3>
          <p className="text-sm text-muted-foreground">{summary}</p>
        </Card>
      )}
      
      {interests.length > 0 && (
        <Card className="p-4">
          <h3 className="font-semibold mb-2">Interests</h3>
          <ScrollArea className="h-[100px]">
            <div className="flex flex-wrap gap-2">
              {interests.map((interest, index) => (
                <Badge key={index} variant="secondary">
                  {interest}
                </Badge>
              ))}
            </div>
          </ScrollArea>
        </Card>
      )}
      
      {accomplishments.length > 0 && (
        <Card className="p-4">
          <h3 className="font-semibold mb-2">Accomplishments</h3>
          <ScrollArea className="h-[100px]">
            <ul className="list-disc list-inside space-y-1">
              {accomplishments.map((accomplishment, index) => (
                <li key={index} className="text-sm">
                  {accomplishment}
                </li>
              ))}
            </ul>
          </ScrollArea>
        </Card>
      )}
      
      {bio && (
        <Card className="p-4">
          <h3 className="font-semibold mb-2">About Me</h3>
          <p className="text-sm text-muted-foreground">{bio}</p>
        </Card>
      )}
      
      {socialLinks && Object.values(socialLinks).some(link => link) && (
        <Card className="p-4">
          <h3 className="font-semibold mb-2">Connect With Me</h3>
          <SocialLinks links={socialLinks} />
        </Card>
      )}
    </div>
  );
}