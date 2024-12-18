import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { toast } from "sonner";
import { ProfileFormValues, profileFormSchema } from "@/lib/validations/profile";
import { FormFields } from "./form/FormFields";
import { FormHeader } from "./form/FormHeader";
import { CodeEditor } from "./CodeEditor";
import { SocialConnections } from "./SocialConnections";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

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

  const handleCodeSave = (html: string, css: string) => {
    onUpdate({ 
      custom_html: html, 
      custom_css: css 
    });
  };

  const handleSocialConnect = (platform: string, accountId: string) => {
    onUpdate({
      connected_accounts: {
        ...profileData.connected_accounts,
        [platform]: accountId
      }
    });
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormHeader />
        
        <Tabs defaultValue="basic" className="w-full">
          <TabsList>
            <TabsTrigger value="basic">Basic Info</TabsTrigger>
            <TabsTrigger value="advanced">Advanced</TabsTrigger>
            <TabsTrigger value="social">Social</TabsTrigger>
          </TabsList>
          
          <TabsContent value="basic">
            <FormFields form={form} onUpdate={onUpdate} />
          </TabsContent>
          
          <TabsContent value="advanced">
            <CodeEditor
              initialHtml={profileData.custom_html}
              initialCss={profileData.custom_css}
              onSave={handleCodeSave}
            />
          </TabsContent>
          
          <TabsContent value="social">
            <SocialConnections
              connectedAccounts={profileData.connected_accounts || {}}
              onConnect={handleSocialConnect}
            />
          </TabsContent>
        </Tabs>

        <Button type="submit" disabled={loading}>
          {loading ? "Saving..." : "Save Changes"}
        </Button>
      </form>
    </Form>
  );
}