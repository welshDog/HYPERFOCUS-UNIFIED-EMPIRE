import { Button } from "@/components/ui/button";
import { Youtube, Instagram, Music2 } from "lucide-react";
import { toast } from "sonner";

interface SocialConnectionsProps {
  connectedAccounts: {
    youtube?: string;
    instagram?: string;
    tiktok?: string;
  };
  onConnect: (platform: string, accountId: string) => void;
}

export function SocialConnections({ connectedAccounts, onConnect }: SocialConnectionsProps) {
  const handleConnect = async (platform: string) => {
    try {
      // This is a placeholder for the actual OAuth flow
      const accountId = `demo-${platform}-${Date.now()}`;
      onConnect(platform, accountId);
      toast.success(`Connected to ${platform} successfully`);
    } catch (error) {
      console.error(`Error connecting to ${platform}:`, error);
      toast.error(`Failed to connect to ${platform}`);
    }
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Connected Accounts</h3>
      
      <div className="grid gap-4">
        <Button
          variant={connectedAccounts.youtube ? "default" : "outline"}
          onClick={() => handleConnect('youtube')}
          className="flex items-center gap-2"
        >
          <Youtube className="h-4 w-4" />
          {connectedAccounts.youtube ? 'YouTube Connected' : 'Connect YouTube'}
        </Button>

        <Button
          variant={connectedAccounts.instagram ? "default" : "outline"}
          onClick={() => handleConnect('instagram')}
          className="flex items-center gap-2"
        >
          <Instagram className="h-4 w-4" />
          {connectedAccounts.instagram ? 'Instagram Connected' : 'Connect Instagram'}
        </Button>

        <Button
          variant={connectedAccounts.tiktok ? "default" : "outline"}
          onClick={() => handleConnect('tiktok')}
          className="flex items-center gap-2"
        >
          <Music2 className="h-4 w-4" />
          {connectedAccounts.tiktok ? 'TikTok Connected' : 'Connect TikTok'}
        </Button>
      </div>
    </div>
  );
}