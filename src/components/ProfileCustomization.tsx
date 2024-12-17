import { useAuth } from "@/contexts/AuthContext";
import { ProfilePreview } from "./ProfilePreview";
import { ProfileDataProvider } from "./profile/customization/ProfileDataProvider";
import { CustomizationForm } from "./profile/customization/CustomizationForm";
import { ErrorBoundary } from "./ErrorBoundary";
import { LoadingBrain } from "./LoadingBrain";

export function ProfileCustomization() {
  const { session } = useAuth();

  return (
    <ErrorBoundary>
      <ProfileDataProvider>
        {({ profileData, loading, handleSave, updateProfileData }) => (
          <div className="grid md:grid-cols-2 gap-8">
            {loading ? (
              <LoadingBrain />
            ) : (
              <>
                <ErrorBoundary>
                  <CustomizationForm
                    profileData={profileData}
                    loading={loading}
                    onSave={handleSave}
                    onUpdate={updateProfileData}
                  />
                </ErrorBoundary>
                
                <div className="space-y-4">
                  <h2 className="text-2xl font-bold">Profile Preview</h2>
                  <ErrorBoundary>
                    <ProfilePreview
                      username={session?.user?.email?.split('@')[0] || 'User'}
                      backgroundType={profileData.background_type}
                      backgroundValue={profileData.background_value}
                      fontFamily={profileData.font_family}
                      fontColor={profileData.font_color}
                      bio={profileData.bio}
                      mood={profileData.mood}
                      playlistUrl={profileData.playlist_url}
                      socialLinks={profileData.social_links}
                    />
                  </ErrorBoundary>
                </div>
              </>
            )}
          </div>
        )}
      </ProfileDataProvider>
    </ErrorBoundary>
  );
}