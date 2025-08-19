import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useToast } from "@/components/ui/use-toast";
import { supabase } from "@/integrations/supabase/client";

export interface ProfileData {
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

interface ProfileDataContextProps {
  children: (props: {
    profileData: ProfileData;
    loading: boolean;
    handleSave: () => Promise<void>;
    updateProfileData: (updates: Partial<ProfileData>) => void;
  }) => React.ReactNode;
}

export function ProfileDataProvider({ children }: ProfileDataContextProps) {
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

  const updateProfileData = (updates: Partial<ProfileData>) => {
    setProfileData(prev => ({ ...prev, ...updates }));
  };

  return children({
    profileData,
    loading,
    handleSave,
    updateProfileData,
  });
}