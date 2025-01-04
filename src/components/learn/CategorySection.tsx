import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { CategoryList } from "./CategoryList";
import { Skeleton } from "@/components/ui/skeleton";

interface CategorySectionProps {
  selectedCategoryId: string | null;
  onCategorySelect: (id: string) => void;
  getCourseCount: (categoryId: string) => number;
}

export const CategorySection = ({
  selectedCategoryId,
  onCategorySelect,
  getCourseCount,
}: CategorySectionProps) => {
  const { data: categories, isLoading } = useQuery({
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

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Array(4).fill(0).map((_, i) => (
          <Skeleton key={i} className="h-48" />
        ))}
      </div>
    );
  }

  return (
    <section className="space-y-6 mb-12">
      <h2 className="text-2xl font-semibold">Categories</h2>
      <CategoryList
        categories={categories ?? []}
        selectedCategoryId={selectedCategoryId}
        onCategorySelect={onCategorySelect}
        courseCount={getCourseCount}
      />
    </section>
  );
};