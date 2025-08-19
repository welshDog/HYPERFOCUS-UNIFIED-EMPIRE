import { formatDistanceToNow } from "date-fns";
import { Heart, MessageCircle, Share2 } from "lucide-react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { useState } from "react";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";

interface PostCardProps {
  id: string;
  content: string;
  image_url?: string | null;
  likes: number;
  created_at: string;
  user: {
    username: string;
    avatar_url?: string | null;
  };
  currentUserId?: string;
}

export function PostCard({ id, content, image_url, likes: initialLikes, created_at, user, currentUserId }: PostCardProps) {
  const [likes, setLikes] = useState(initialLikes || 0);
  const [isLiking, setIsLiking] = useState(false);

  const handleLike = async () => {
    if (!currentUserId) {
      toast.error("Please sign in to like posts");
      return;
    }

    setIsLiking(true);
    try {
      const { error } = await supabase
        .from('posts')
        .update({ likes: likes + 1 })
        .eq('id', id);

      if (error) throw error;
      setLikes(prev => prev + 1);
      console.log("Post liked successfully");
    } catch (error) {
      console.error("Error liking post:", error);
      toast.error("Failed to like post");
    } finally {
      setIsLiking(false);
    }
  };

  return (
    <Card className="p-6 space-y-4">
      <div className="flex items-start space-x-4">
        <Avatar className="w-10 h-10">
          <AvatarImage src={user.avatar_url || ''} alt={user.username} />
          <AvatarFallback>{user.username[0]?.toUpperCase()}</AvatarFallback>
        </Avatar>
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold">{user.username}</h3>
            <span className="text-sm text-muted-foreground">
              {formatDistanceToNow(new Date(created_at), { addSuffix: true })}
            </span>
          </div>
          <p className="mt-2 text-gray-700">{content}</p>
          {image_url && (
            <img
              src={image_url}
              alt="Post attachment"
              className="mt-4 rounded-lg max-h-96 w-full object-cover"
            />
          )}
        </div>
      </div>
      
      <div className="flex items-center justify-between pt-4 border-t">
        <Button
          variant="ghost"
          size="sm"
          className="flex items-center space-x-2"
          onClick={handleLike}
          disabled={isLiking}
        >
          <Heart className="w-4 h-4" />
          <span>{likes}</span>
        </Button>
        <Button variant="ghost" size="sm" className="flex items-center space-x-2">
          <MessageCircle className="w-4 h-4" />
          <span>Comment</span>
        </Button>
        <Button variant="ghost" size="sm" className="flex items-center space-x-2">
          <Share2 className="w-4 h-4" />
          <span>Share</span>
        </Button>
      </div>
    </Card>
  );
}