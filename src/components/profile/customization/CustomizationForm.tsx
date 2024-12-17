import { Button } from "@/components/ui/button";
import { BackgroundSection } from "../BackgroundSection";
import { FontSection } from "../FontSection";
import { BioSection } from "../BioSection";
import { MusicSection } from "../MusicSection";
import { SocialSection } from "../SocialSection";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { ProfileData } from "./ProfileDataProvider";
import { Skeleton } from "@/components/ui/skeleton";

interface CustomizationFormProps {
  profileData: ProfileData;
  loading: boolean;
  onSave: () => Promise<void>;
  onUpdate: (updates: Partial<ProfileData>) => void;
}

export function CustomizationForm({
  profileData,
  loading,
  onSave,
  onUpdate,
}: CustomizationFormProps) {
  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-32" />
        <Skeleton className="h-24" />
        <Skeleton className="h-24" />
        <Skeleton className="h-16" />
        <Skeleton className="h-24" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-2xl font-bold">Customize Your Profile</h2>
        <p className="text-muted-foreground">Make your profile uniquely yours!</p>
      </div>

      <BackgroundSection
        backgroundType={profileData.background_type}
        backgroundValue={profileData.background_value}
        onChange={(type, value) => onUpdate({
          background_type: type,
          background_value: value
        })}
      />

      <FontSection
        fontFamily={profileData.font_family}
        fontColor={profileData.font_color}
        onFontFamilyChange={(value) => onUpdate({
          font_family: value
        })}
        onFontColorChange={(value) => onUpdate({
          font_color: value
        })}
      />

      <BioSection
        bio={profileData.bio}
        onChange={(value) => onUpdate({
          bio: value
        })}
      />

      <div className="space-y-4">
        <Label>Current Mood</Label>
        <Input
          placeholder="How are you feeling?"
          value={profileData.mood}
          onChange={(e) => onUpdate({
            mood: e.target.value
          })}
        />
      </div>

      <MusicSection
        playlistUrl={profileData.playlist_url}
        onChange={(value) => onUpdate({
          playlist_url: value
        })}
      />

      <SocialSection
        socialLinks={profileData.social_links}
        onChange={(platform, value) => onUpdate({
          social_links: {
            ...profileData.social_links,
            [platform]: value
          }
        })}
      />

      <Button
        onClick={onSave}
        disabled={loading}
        className="w-full"
      >
        {loading ? 'Saving...' : 'Save Changes'}
      </Button>
    </div>
  );
}