import { Sidebar } from "@/components/Sidebar";
import { CourseCard } from "@/components/CourseCard";
import { CategoryCard } from "@/components/CategoryCard";
import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { useState } from "react";

export default function Learn() {
  const [selectedCategoryId, setSelectedCategoryId] = useState<string | null>(null);

  const { data: categories, isLoading: categoriesLoading } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => {
      console.log("Fetching categories...");
      const { data, error } = await supabase
        .from('categories')
        .select('*');
      
      if (error) {
        console.error("Error fetching categories:", error);
        throw error;
      }
      
      console.log("Categories fetched:", data);
      return data;
    },
  });

  const { data: courses, isLoading: coursesLoading } = useQuery({
    queryKey: ['courses', selectedCategoryId],
    queryFn: async () => {
      console.log("Fetching courses...");
      let query = supabase
        .from('courses')
        .select('*, categories_courses!inner(category_id)');
      
      if (selectedCategoryId) {
        query = query.eq('categories_courses.category_id', selectedCategoryId);
      }
      
      const { data, error } = await query;
      
      if (error) {
        console.error("Error fetching courses:", error);
        throw error;
      }
      
      console.log("Courses fetched:", data);
      return data;
    },
  });

  if (categoriesLoading || coursesLoading) {
    return (
      <div className="flex h-screen bg-background">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-8">
          <h1 className="text-4xl font-bold mb-8">Learn</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Array(4).fill(0).map((_, i) => (
              <Skeleton key={i} className="h-48" />
            ))}
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-4xl font-bold mb-8">Learn</h1>
        
        {/* Categories section */}
        <section className="space-y-6 mb-12">
          <h2 className="text-2xl font-semibold">Categories</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {categories?.map((category) => (
              <CategoryCard
                key={category.id}
                category={category}
                courseCount={courses?.filter(
                  course => course.categories_courses.some(
                    cc => cc.category_id === category.id
                  )
                ).length}
                onClick={() => setSelectedCategoryId(
                  selectedCategoryId === category.id ? null : category.id
                )}
                className={selectedCategoryId === category.id ? "ring-2 ring-primary" : ""}
              />
            ))}
          </div>
        </section>
        
        {/* Courses section */}
        <section className="space-y-6">
          <h2 className="text-2xl font-semibold">
            {selectedCategoryId 
              ? `Courses in ${categories?.find(c => c.id === selectedCategoryId)?.name}`
              : "All Courses"}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {courses?.length ? (
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
      </main>
    </div>
  );
}