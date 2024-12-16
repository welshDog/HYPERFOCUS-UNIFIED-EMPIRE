import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Music, Palette, Image, Link as LinkIcon } from "lucide-react";
import { supabase } from "@/integrations/supabase/client";

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
      console.log('Profile updated successfully');
    } catch (error) {
      console.error('Error updating profile:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 p-4 max-w-2xl mx-auto">
      <div className="space-y-2">
        <h2 className="text-2xl font-bold">Customize Your Profile</h2>
        <p className="text-muted-foreground">Make your profile uniquely yours!</p>
      </div>

      {/* Background Section */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <Palette className="h-5 w-5" />
          <h3 className="text-lg font-semibold">Background</h3>
        </div>
        <div className="grid gap-4">
          <div className="flex items-center gap-4">
            <Label>
              <input
                type="radio"
                name="background_type"
                value="color"
                checked={profileData.background_type === 'color'}
                onChange={(e) => setProfileData({
                  ...profileData,
                  background_type: 'color'
                })}
                className="mr-2"
              />
              Color
            </Label>
            <Label>
              <input
                type="radio"
                name="background_type"
                value="image"
                checked={profileData.background_type === 'image'}
                onChange={(e) => setProfileData({
                  ...profileData,
                  background_type: 'image'
                })}
                className="mr-2"
              />
              Image
            </Label>
          </div>
          {profileData.background_type === 'color' ? (
            <Input
              type="color"
              value={profileData.background_value}
              onChange={(e) => setProfileData({
                ...profileData,
                background_value: e.target.value
              })}
            />
          ) : (
            <Input
              type="url"
              placeholder="Enter image URL"
              value={profileData.background_value}
              onChange={(e) => setProfileData({
                ...profileData,
                background_value: e.target.value
              })}
            />
          )}
        </div>
      </div>

      {/* Font Customization */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <span className="text-lg">Aa</span>
          <h3 className="text-lg font-semibold">Font Settings</h3>
        </div>
        <div className="grid gap-4">
          <div>
            <Label>Font Family</Label>
            <select
              className="w-full p-2 border rounded-md"
              value={profileData.font_family}
              onChange={(e) => setProfileData({
                ...profileData,
                font_family: e.target.value
              })}
            >
              <option value="Inter">Inter</option>
              <option value="Arial">Arial</option>
              <option value="Times New Roman">Times New Roman</option>
              <option value="Comic Sans MS">Comic Sans MS</option>
            </select>
          </div>
          <div>
            <Label>Font Color</Label>
            <Input
              type="color"
              value={profileData.font_color}
              onChange={(e) => setProfileData({
                ...profileData,
                font_color: e.target.value
              })}
            />
          </div>
        </div>
      </div>

      {/* Bio Section */}
      <div className="space-y-4">
        <Label>About Me</Label>
        <Textarea
          placeholder="Tell us about yourself..."
          value={profileData.bio}
          onChange={(e) => setProfileData({
            ...profileData,
            bio: e.target.value
          })}
          className="min-h-[100px]"
        />
      </div>

      {/* Mood */}
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

      {/* Music Playlist */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <Music className="h-5 w-5" />
          <Label>Music Playlist URL</Label>
        </div>
        <Input
          placeholder="Spotify or YouTube playlist URL"
          value={profileData.playlist_url}
          onChange={(e) => setProfileData({
            ...profileData,
            playlist_url: e.target.value
          })}
        />
      </div>

      {/* Social Links */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <LinkIcon className="h-5 w-5" />
          <h3 className="text-lg font-semibold">Social Links</h3>
        </div>
        <div className="grid gap-4">
          <div>
            <Label>Twitter</Label>
            <Input
              placeholder="Twitter profile URL"
              value={profileData.social_links.twitter || ''}
              onChange={(e) => setProfileData({
                ...profileData,
                social_links: {
                  ...profileData.social_links,
                  twitter: e.target.value
                }
              })}
            />
          </div>
          <div>
            <Label>Instagram</Label>
            <Input
              placeholder="Instagram profile URL"
              value={profileData.social_links.instagram || ''}
              onChange={(e) => setProfileData({
                ...profileData,
                social_links: {
                  ...profileData.social_links,
                  instagram: e.target.value
                }
              })}
            />
          </div>
          <div>
            <Label>GitHub</Label>
            <Input
              placeholder="GitHub profile URL"
              value={profileData.social_links.github || ''}
              onChange={(e) => setProfileData({
                ...profileData,
                social_links: {
                  ...profileData.social_links,
                  github: e.target.value
                }
              })}
            />
          </div>
        </div>
      </div>

      <Button
        onClick={handleSave}
        disabled={loading}
        className="w-full"
      >
        {loading ? 'Saving...' : 'Save Changes'}
      </Button>
    </div>
  );
}