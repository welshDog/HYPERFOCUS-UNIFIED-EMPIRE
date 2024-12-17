import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Button } from "@/components/ui/button"
import { BackgroundSection } from "../BackgroundSection"
import { FontSection } from "../FontSection"
import { BioSection } from "../BioSection"
import { MusicSection } from "../MusicSection"
import { SocialSection } from "../SocialSection"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import type { ProfileData } from "./ProfileDataProvider"
import { profileFormSchema, type ProfileFormValues } from "@/lib/validations/profile"
import { useToast } from "@/components/ui/use-toast"

interface CustomizationFormProps {
  profileData: ProfileData
  loading: boolean
  onSave: () => Promise<void>
  onUpdate: (updates: Partial<ProfileData>) => void
}

export function CustomizationForm({
  profileData,
  loading,
  onSave,
  onUpdate,
}: CustomizationFormProps) {
  const { toast } = useToast()
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
      social_links: profileData.social_links
    }
  })

  const handleSubmit = async (values: ProfileFormValues) => {
    try {
      onUpdate(values)
      await onSave()
      toast({
        title: "Success",
        description: "Profile updated successfully",
      })
    } catch (error) {
      console.error("Error saving profile:", error)
      toast({
        title: "Error",
        description: "Failed to save profile changes",
        variant: "destructive",
      })
    }
  }

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
    )
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">Customize Your Profile</h2>
          <p className="text-muted-foreground">Make your profile uniquely yours!</p>
        </div>

        <FormField
          control={form.control}
          name="background_type"
          render={({ field }) => (
            <FormItem>
              <BackgroundSection
                backgroundType={field.value}
                backgroundValue={form.watch("background_value")}
                onChange={(type, value) => {
                  form.setValue("background_type", type)
                  form.setValue("background_value", value)
                }}
              />
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="font_family"
          render={({ field }) => (
            <FormItem>
              <FontSection
                fontFamily={field.value}
                fontColor={form.watch("font_color")}
                onFontFamilyChange={(value) => form.setValue("font_family", value)}
                onFontColorChange={(value) => form.setValue("font_color", value)}
              />
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="bio"
          render={({ field }) => (
            <FormItem>
              <BioSection
                bio={field.value}
                onChange={(value) => form.setValue("bio", value)}
              />
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="mood"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Current Mood</FormLabel>
              <FormControl>
                <Input
                  placeholder="How are you feeling?"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="playlist_url"
          render={({ field }) => (
            <FormItem>
              <MusicSection
                playlistUrl={field.value}
                onChange={(value) => form.setValue("playlist_url", value)}
              />
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="social_links"
          render={({ field }) => (
            <FormItem>
              <SocialSection
                socialLinks={field.value}
                onChange={(platform, value) =>
                  form.setValue(`social_links.${platform}`, value)
                }
              />
              <FormMessage />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          disabled={loading}
          className="w-full"
        >
          {loading ? "Saving..." : "Save Changes"}
        </Button>
      </form>
    </Form>
  )
}