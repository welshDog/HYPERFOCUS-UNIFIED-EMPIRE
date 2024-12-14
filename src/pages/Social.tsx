import { Sidebar } from "@/components/Sidebar";
import { PostCard } from "@/components/PostCard";
import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { useEffect, useState } from "react";

type PostWithProfile = {
  id: string;
  content: string;
  image_url: string | null;
  likes: number | null;
  created_at: string;
  user: {
    username: string | null;
    avatar_url: string | null;
  };
};

// Add a type for the raw response from Supabase
type PostResponse = {
  id: string;
  content: string;
  image_url: string | null;
  likes: number | null;
  created_at: string;
  user_id: string;
  profile: {
    username: string | null;
    avatar_url: string | null;
  }[];
};

export default function Social() {
  const [currentUserId, setCurrentUserId] = useState<string | undefined>();

  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      setCurrentUserId(session?.user.id);
    });

    return () => subscription.unsubscribe();
  }, []);

  const { data: posts, isLoading, error } = useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      console.log("Fetching posts...");
      const { data: postsData, error: postsError } = await supabase
        .from('posts')
        .select(`
          id,
          content,
          image_url,
          likes,
          created_at,
          user_id,
          profile:profiles(username, avatar_url)
        `)
        .order('created_at', { ascending: false });

      if (postsError) {
        console.error("Error fetching posts:", postsError);
        throw postsError;
      }

      // Transform the data to match our expected type
      const transformedPosts = (postsData || []).map(post => ({
        ...post,
        user: {
          username: post.profile[0]?.username ?? null,
          avatar_url: post.profile[0]?.avatar_url ?? null
        }
      })) as PostWithProfile[];

      console.log("Posts fetched:", transformedPosts);
      return transformedPosts;
    },
  });

  if (error) {
    toast.error("Failed to load posts");
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-4xl font-bold mb-8">Community</h1>
        
        {/* Social feed section */}
        <section className="max-w-2xl mx-auto space-y-6">
          <h2 className="text-2xl font-semibold">Social Feed</h2>
          
          {isLoading ? (
            // Loading skeletons
            Array(3).fill(0).map((_, i) => (
              <div key={i} className="space-y-4">
                <Skeleton className="h-48 w-full" />
              </div>
            ))
          ) : posts?.length ? (
            posts.map((post) => (
              <PostCard
                key={post.id}
                id={post.id}
                content={post.content}
                image_url={post.image_url}
                likes={post.likes}
                created_at={post.created_at}
                user={post.user}
                currentUserId={currentUserId}
              />
            ))
          ) : (
            <p className="text-center text-muted-foreground">
              No posts available yet.
            </p>
          )}
        </section>
      </main>
    </div>
  );
}