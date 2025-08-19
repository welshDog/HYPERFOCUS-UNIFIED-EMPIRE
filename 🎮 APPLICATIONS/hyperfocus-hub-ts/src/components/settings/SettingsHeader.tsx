import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useAuth } from "@/contexts/AuthContext";

export function SettingsHeader() {
  const { session } = useAuth();
  const email = session?.user?.email;
  const username = email?.split('@')[0] || 'User';

  return (
    <div className="flex items-center space-x-4 p-4 border-b">
      <Avatar className="h-12 w-12">
        <AvatarImage src="/placeholder.svg" alt={username} />
        <AvatarFallback>{username[0]?.toUpperCase()}</AvatarFallback>
      </Avatar>
      <div>
        <h2 className="text-lg font-semibold">{username}</h2>
        <p className="text-sm text-muted-foreground">{email}</p>
      </div>
    </div>
  );
}