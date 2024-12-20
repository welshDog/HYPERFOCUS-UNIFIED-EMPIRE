import { FormField } from "@/components/ui/form";
import { BackgroundSection } from "../../BackgroundSection";
import { FontSection } from "../../FontSection";
import { BioSection } from "../../BioSection";
import { MusicSection } from "../../MusicSection";
import { SocialSection } from "../../SocialSection";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { PlusCircle, X } from "lucide-react";
import { FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form";
import { UseFormReturn } from "react-hook-form";
import type { ProfileFormValues } from "@/lib/validations/profile";

interface FormFieldsProps {
  form: UseFormReturn<ProfileFormValues>;
  onUpdate: (data: Partial<ProfileFormValues>) => void;
}

export function FormFields({ form, onUpdate }: FormFieldsProps) {
  const handleAddInterest = () => {
    const currentInterests = form.watch("interests") || [];
    form.setValue("interests", [...currentInterests, ""]);
  };

  const handleAddAccomplishment = () => {
    const currentAccomplishments = form.watch("accomplishments") || [];
    form.setValue("accomplishments", [...currentAccomplishments, ""]);
  };

  const handleRemoveInterest = (index: number) => {
    const currentInterests = form.watch("interests") || [];
    const newInterests = currentInterests.filter((_, i) => i !== index);
    form.setValue("interests", newInterests);
    onUpdate({ interests: newInterests });
  };

  const handleRemoveAccomplishment = (index: number) => {
    const currentAccomplishments = form.watch("accomplishments") || [];
    const newAccomplishments = currentAccomplishments.filter((_, i) => i !== index);
    form.setValue("accomplishments", newAccomplishments);
    onUpdate({ accomplishments: newAccomplishments });
  };

  return (
    <div className="space-y-8">
      <FormField
        control={form.control}
        name="summary"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Summary</FormLabel>
            <FormControl>
              <Textarea
                placeholder="Write a brief summary about yourself..."
                {...field}
                onChange={(e) => {
                  field.onChange(e);
                  onUpdate({ summary: e.target.value });
                }}
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />

      <div>
        <FormLabel>Interests</FormLabel>
        <div className="space-y-2">
          {(form.watch("interests") || []).map((interest, index) => (
            <div key={index} className="flex gap-2">
              <Input
                value={interest}
                onChange={(e) => {
                  const newInterests = [...(form.watch("interests") || [])];
                  newInterests[index] = e.target.value;
                  form.setValue("interests", newInterests);
                  onUpdate({ interests: newInterests });
                }}
                placeholder="Enter an interest..."
              />
              <Button
                type="button"
                variant="ghost"
                size="icon"
                onClick={() => handleRemoveInterest(index)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          ))}
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={handleAddInterest}
            className="mt-2"
          >
            <PlusCircle className="h-4 w-4 mr-2" />
            Add Interest
          </Button>
        </div>
      </div>

      <div>
        <FormLabel>Accomplishments</FormLabel>
        <div className="space-y-2">
          {(form.watch("accomplishments") || []).map((accomplishment, index) => (
            <div key={index} className="flex gap-2">
              <Input
                value={accomplishment}
                onChange={(e) => {
                  const newAccomplishments = [...(form.watch("accomplishments") || [])];
                  newAccomplishments[index] = e.target.value;
                  form.setValue("accomplishments", newAccomplishments);
                  onUpdate({ accomplishments: newAccomplishments });
                }}
                placeholder="Enter an accomplishment..."
              />
              <Button
                type="button"
                variant="ghost"
                size="icon"
                onClick={() => handleRemoveAccomplishment(index)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          ))}
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={handleAddAccomplishment}
            className="mt-2"
          >
            <PlusCircle className="h-4 w-4 mr-2" />
            Add Accomplishment
          </Button>
        </div>
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
                form.setValue("background_type", type);
                form.setValue("background_value", value);
                onUpdate({ background_type: type, background_value: value });
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
              onFontFamilyChange={(value) => {
                form.setValue("font_family", value);
                onUpdate({ font_family: value });
              }}
              onFontColorChange={(value) => {
                form.setValue("font_color", value);
                onUpdate({ font_color: value });
              }}
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
              onChange={(value) => {
                form.setValue("bio", value);
                onUpdate({ bio: value });
              }}
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
                onChange={(e) => {
                  field.onChange(e);
                  onUpdate({ mood: e.target.value });
                }}
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
              onChange={(value) => {
                form.setValue("playlist_url", value);
                onUpdate({ playlist_url: value });
              }}
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
              onChange={(platform, value) => {
                form.setValue(`social_links.${platform}`, value);
                onUpdate({ 
                  social_links: {
                    ...field.value,
                    [platform]: value
                  }
                });
              }}
            />
            <FormMessage />
          </FormItem>
        )}
      />
    </div>
  );
}
