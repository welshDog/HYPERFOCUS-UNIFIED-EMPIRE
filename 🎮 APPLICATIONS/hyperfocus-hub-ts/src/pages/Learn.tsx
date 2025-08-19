import { useState, useCallback } from "react";
import { Sidebar } from "@/components/Sidebar";
import { AppErrorBoundary } from "@/components/AppErrorBoundary";
import { CategorySection } from "@/components/learn/CategorySection";
import { CourseSection } from "@/components/learn/CourseSection";

export default function Learn() {
  const [selectedCategoryId, setSelectedCategoryId] = useState<string | null>(null);

  const handleCategorySelect = useCallback((id: string) => {
    setSelectedCategoryId(prevId => prevId === id ? null : id);
  }, []);

  const getCourseCount = useCallback((categoryId: string) => {
    // This will be updated automatically by React Query when courses data changes
    return courses?.filter(
      course => course.categories_courses.some(
        cc => cc.category_id === categoryId
      )
    ).length ?? 0;
  }, [courses]);

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <AppErrorBoundary>
          <h1 className="text-4xl font-bold mb-8">Learn</h1>
          
          <CategorySection
            selectedCategoryId={selectedCategoryId}
            onCategorySelect={handleCategorySelect}
            getCourseCount={getCourseCount}
          />
          
          <CourseSection
            selectedCategoryId={selectedCategoryId}
          />
        </AppErrorBoundary>
      </main>
    </div>
  );
}