import { Avatar } from "@/components/ui/avatar";

interface ProfileHeaderProps {
  username: string;
  avatarUrl?: string;
  mood?: string;
}

export function ProfileHeader({ username, avatarUrl, mood }: ProfileHeaderProps) {
  return (
    <div className="flex items-center gap-4 mb-6">
      <Avatar className="h-20 w-20">
        <img
          src={avatarUrl || "/placeholder.svg"}
          alt={username}
          className="h-full w-full object-cover"
        />
      </Avatar>
      <div>
        <h2 className="text-2xl font-bold">{username}</h2>
        {mood && <p className="text-muted-foreground">Feeling: {mood}</p>}
      </div>
    </div>
  );
}