import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Form } from "@/components/ui/form";
import type { ProfileData } from "./ProfileDataProvider";
import { profileFormSchema, type ProfileFormValues } from "@/lib/validations/profile";
import { useToast } from "@/components/ui/use-toast";
import { FormHeader } from "./form/FormHeader";
import { FormFields } from "./form/FormFields";

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
  const { toast } = useToast();
  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    defaultValues: {
      background_type: profileData.background_type,
      background_value: profileData.background_value,
      font_family: profileData.font_family,
      font_color: profileData.font_color,
      bio: profileData.bio,
      mood: profileData.mood,
      playlist_url: profileData.playlist_url,
      social_links: profileData.social_links,
    },
  });

  const handleSubmit = async (values: ProfileFormValues) => {
    try {
      onUpdate(values);
      await onSave();
      toast({
        title: "Success",
        description: "Profile updated successfully",
      });
    } catch (error) {
      console.error("Error saving profile:", error);
      toast({
        title: "Error",
        description: "Failed to save profile changes",
        variant: "destructive",
      });
    }
  };

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
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
        <FormHeader />
        <FormFields form={form} />
        <Button
          type="submit"
          disabled={loading}
          className="w-full"
        >
          {loading ? "Saving..." : "Save Changes"}
        </Button>
      </form>
    </Form>
  );
}