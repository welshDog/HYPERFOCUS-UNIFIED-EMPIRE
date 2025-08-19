import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { Brain, BookOpen, Clock, Lightbulb } from "lucide-react";
import { type Database } from "@/integrations/supabase/types";

type Category = Database["public"]["Tables"]["categories"]["Row"];

const iconMap = {
  brain: Brain,
  "book-open": BookOpen,
  clock: Clock,
  lightbulb: Lightbulb,
};

interface CategoryCardProps {
  category: Category;
  courseCount?: number;
  className?: string;
  onClick?: () => void;
}

export function CategoryCard({ category, courseCount = 0, className, onClick }: CategoryCardProps) {
  const IconComponent = category.icon ? iconMap[category.icon as keyof typeof iconMap] : Brain;

  return (
    <Card 
      className={cn(
        "group cursor-pointer transition-all duration-300 hover:shadow-lg dark:hover:shadow-primary/5",
        className
      )}
      onClick={onClick}
    >
      <CardHeader>
        <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary group-hover:bg-primary group-hover:text-primary-foreground">
          <IconComponent className="h-6 w-6" />
        </div>
        <CardTitle className="line-clamp-1">{category.name}</CardTitle>
        <CardDescription className="line-clamp-2">{category.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">
          {courseCount} {courseCount === 1 ? 'Course' : 'Courses'}
        </p>
      </CardContent>
    </Card>
  );
}