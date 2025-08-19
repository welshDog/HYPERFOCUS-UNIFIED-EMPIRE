import { memo } from "react";
import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { CourseList } from "./CourseList";
import { Skeleton } from "@/components/ui/skeleton";

interface CourseSectionProps {
  selectedCategoryId: string | null;
}

export const CourseSection = memo(({ selectedCategoryId }: CourseSectionProps) => {
  const { data: courses, isLoading } = useQuery({
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

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array(6).fill(0).map((_, i) => (
          <Skeleton key={i} className="h-48" />
        ))}
      </div>
    );
  }

  return (
    <CourseList
      courses={courses ?? []}
      selectedCategory={selectedCategoryId}
    />
  );
});

CourseSection.displayName = "CourseSection";