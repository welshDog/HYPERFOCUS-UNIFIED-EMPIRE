import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { toast } from "@/components/ui/use-toast";
import { ProfileFormValues, profileFormSchema } from "@/lib/validations/profile";
import { FormFields } from "./form/FormFields";
import { FormHeader } from "./form/FormHeader";

interface CustomizationFormProps {
  profileData: ProfileFormValues;
  loading: boolean;
  onSave: (data: ProfileFormValues) => Promise<void>;
  onUpdate: (data: Partial<ProfileFormValues>) => void;
}

export function CustomizationForm({
  profileData,
  loading,
  onSave,
  onUpdate,
}: CustomizationFormProps) {
  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    defaultValues: profileData,
  });

  async function onSubmit(data: ProfileFormValues) {
    try {
      await onSave(data);
      toast({
        title: "Profile updated",
        description: "Your profile has been updated successfully.",
      });
    } catch (error) {
      console.error("Error saving profile:", error);
      toast({
        title: "Error",
        description: "Failed to update profile. Please try again.",
        variant: "destructive",
      });
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormHeader />
        <FormFields form={form} onUpdate={onUpdate} />
        <Button type="submit" disabled={loading}>
          {loading ? "Saving..." : "Save Changes"}
        </Button>
      </form>
    </Form>
  );
}