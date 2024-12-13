import { Sidebar } from "@/components/Sidebar";
import { CourseCard } from "@/components/CourseCard";
import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";

export default function Learn() {
  const { data: courses, isLoading, error } = useQuery({
    queryKey: ['courses'],
    queryFn: async () => {
      console.log("Fetching courses...");
      const { data, error } = await supabase
        .from('courses')
        .select('*')
        .order('created_at', { ascending: false });
      
      if (error) {
        console.error("Error fetching courses:", error);
        throw error;
      }
      
      console.log("Courses fetched:", data);
      return data;
    },
  });

  if (error) {
    toast.error("Failed to load courses");
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-4xl font-bold mb-8">Learn</h1>
        
        {/* Your Courses section */}
        <section className="space-y-6 mb-12">
          <h2 className="text-2xl font-semibold">Your Courses</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {isLoading ? (
              // Loading skeletons
              Array(3).fill(0).map((_, i) => (
                <div key={i} className="space-y-4">
                  <Skeleton className="h-48 w-full" />
                  <Skeleton className="h-4 w-3/4" />
                  <Skeleton className="h-4 w-1/2" />
                </div>
              ))
            ) : courses?.length ? (
              courses.map((course) => (
                <CourseCard
                  key={course.id}
                  title={course.title}
                  description={course.description}
                  duration={course.duration}
                  difficulty={course.difficulty}
                  rating={course.rating}
                  image_url={course.image_url}
                />
              ))
            ) : (
              <p className="col-span-full text-center text-muted-foreground">
                No courses available yet.
              </p>
            )}
          </div>
        </section>
        
        {/* Recommended Courses section */}
        <section className="space-y-6">
          <h2 className="text-2xl font-semibold">Recommended for You</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {isLoading ? (
              // Loading skeletons
              Array(3).fill(0).map((_, i) => (
                <div key={i} className="space-y-4">
                  <Skeleton className="h-48 w-full" />
                  <Skeleton className="h-4 w-3/4" />
                  <Skeleton className="h-4 w-1/2" />
                </div>
              ))
            ) : courses?.length ? (
              // For now, showing the same courses in recommended
              // In a real app, you'd implement recommendation logic
              courses.slice(0, 3).map((course) => (
                <CourseCard
                  key={course.id}
                  title={course.title}
                  description={course.description}
                  duration={course.duration}
                  difficulty={course.difficulty}
                  rating={course.rating}
                  image_url={course.image_url}
                />
              ))
            ) : (
              <p className="col-span-full text-center text-muted-foreground">
                No recommendations available yet.
              </p>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}