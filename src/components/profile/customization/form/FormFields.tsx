import { FormField } from "@/components/ui/form";
import { BackgroundSection } from "../../BackgroundSection";
import { FontSection } from "../../FontSection";
import { BioSection } from "../../BioSection";
import { MusicSection } from "../../MusicSection";
import { SocialSection } from "../../SocialSection";
import { Input } from "@/components/ui/input";
import { FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form";
import { UseFormReturn } from "react-hook-form";
import type { ProfileFormValues } from "@/lib/validations/profile";

interface FormFieldsProps {
  form: UseFormReturn<ProfileFormValues>;
}

export function FormFields({ form }: FormFieldsProps) {
  return (
    <>
      <FormField
        control={form.control}
        name="background_type"
        render={({ field }) => (
          <FormItem>
            <BackgroundSection
              backgroundType={field.value}
              backgroundValue={form.watch("background_value")}
              onChange={(type, value) => {
                form.setValue("background_type", type);
                form.setValue("background_value", value);
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
    </>
  );
}