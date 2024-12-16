import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/use-toast";
import { supabase } from "@/integrations/supabase/client";
import { ProfilePreview } from "./ProfilePreview";
import { BackgroundSection } from "./profile/BackgroundSection";
import { FontSection } from "./profile/FontSection";
import { BioSection } from "./profile/BioSection";
import { MusicSection } from "./profile/MusicSection";
import { SocialSection } from "./profile/SocialSection";

interface ProfileData {
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
}

export function ProfileCustomization() {
  const { session } = useAuth();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const [profileData, setProfileData] = useState<ProfileData>({
    background_type: 'color',
    background_value: '#FFFFFF',
    font_family: 'Inter',
    font_color: '#000000',
    bio: '',
    mood: '',
    playlist_url: '',
    social_links: {},
  });

  const handleSave = async () => {
    try {
      setLoading(true);
      const { error } = await supabase
        .from('profiles')
        .update({
          background_type: profileData.background_type,
          background_value: profileData.background_value,
          font_family: profileData.font_family,
          font_color: profileData.font_color,
          bio: profileData.bio,
          mood: profileData.mood,
          playlist_url: profileData.playlist_url,
          social_links: profileData.social_links,
        })
        .eq('id', session?.user.id);

      if (error) throw error;
      toast({
        title: "Success",
        description: "Profile updated successfully",
      });
    } catch (error) {
      console.error('Error updating profile:', error);
      toast({
        title: "Error",
        description: "Failed to update profile",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid md:grid-cols-2 gap-8">
      <div className="space-y-6">
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">Customize Your Profile</h2>
          <p className="text-muted-foreground">Make your profile uniquely yours!</p>
        </div>

        <BackgroundSection
          backgroundType={profileData.background_type}
          backgroundValue={profileData.background_value}
          onChange={(type, value) => setProfileData({
            ...profileData,
            background_type: type,
            background_value: value
          })}
        />

        <FontSection
          fontFamily={profileData.font_family}
          fontColor={profileData.font_color}
          onFontFamilyChange={(value) => setProfileData({
            ...profileData,
            font_family: value
          })}
          onFontColorChange={(value) => setProfileData({
            ...profileData,
            font_color: value
          })}
        />

        <BioSection
          bio={profileData.bio}
          onChange={(value) => setProfileData({
            ...profileData,
            bio: value
          })}
        />

        <div className="space-y-4">
          <Label>Current Mood</Label>
          <Input
            placeholder="How are you feeling?"
            value={profileData.mood}
            onChange={(e) => setProfileData({
              ...profileData,
              mood: e.target.value
            })}
          />
        </div>

        <MusicSection
          playlistUrl={profileData.playlist_url}
          onChange={(value) => setProfileData({
            ...profileData,
            playlist_url: value
          })}
        />

        <SocialSection
          socialLinks={profileData.social_links}
          onChange={(platform, value) => setProfileData({
            ...profileData,
            social_links: {
              ...profileData.social_links,
              [platform]: value
            }
          })}
        />

        <Button
          onClick={handleSave}
          disabled={loading}
          className="w-full"
        >
          {loading ? 'Saving...' : 'Save Changes'}
        </Button>
      </div>

      <div className="space-y-4">
        <h2 className="text-2xl font-bold">Profile Preview</h2>
        <ProfilePreview profileData={profileData} />
      </div>
    </div>
  );
}