import { CategoryCard } from "@/components/CategoryCard";
import { type Database } from "@/integrations/supabase/types";

type Category = Database["public"]["Tables"]["categories"]["Row"];

interface CategoryListProps {
  categories: Category[];
  selectedCategoryId: string | null;
  onCategorySelect: (categoryId: string) => void;
  courseCount: (categoryId: string) => number;
}

export const CategoryList = ({
  categories,
  selectedCategoryId,
  onCategorySelect,
  courseCount,
}: CategoryListProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {categories?.map((category) => (
        <CategoryCard
          key={category.id}
          category={category}
          courseCount={courseCount(category.id)}
          onClick={() => onCategorySelect(category.id)}
          className={selectedCategoryId === category.id ? "ring-2 ring-primary" : ""}
        />
      ))}
    </div>
  );
};