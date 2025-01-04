import { Sidebar } from "@/components/Sidebar";
import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { Skeleton } from "@/components/ui/skeleton";
import { useState } from "react";
import { CategoryList } from "@/components/learn/CategoryList";
import { CourseList } from "@/components/learn/CourseList";
import { AppErrorBoundary } from "@/components/AppErrorBoundary";

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

  const getCourseCount = (categoryId: string) => {
    return courses?.filter(
      course => course.categories_courses.some(
        cc => cc.category_id === categoryId
      )
    ).length ?? 0;
  };

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
        <AppErrorBoundary>
          <h1 className="text-4xl font-bold mb-8">Learn</h1>
          
          <section className="space-y-6 mb-12">
            <h2 className="text-2xl font-semibold">Categories</h2>
            <CategoryList
              categories={categories ?? []}
              selectedCategoryId={selectedCategoryId}
              onCategorySelect={(id) => setSelectedCategoryId(
                selectedCategoryId === id ? null : id
              )}
              courseCount={getCourseCount}
            />
          </section>
          
          <CourseList
            courses={courses ?? []}
            selectedCategory={selectedCategoryId}
          />
        </AppErrorBoundary>
      </main>
    </div>
  );
}