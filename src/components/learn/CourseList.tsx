import { memo } from "react";
import { CourseCard } from "@/components/CourseCard";

interface Course {
  id: string;
  title: string;
  description: string;
  duration: string;
  difficulty: string;
  rating: number;
  image_url: string;
}

interface CourseListProps {
  courses: Course[];
  selectedCategory: string | null;
}

export const CourseList = memo(({ courses, selectedCategory }: CourseListProps) => {
  const categoryName = selectedCategory 
    ? courses.find(c => c.id === selectedCategory)?.title 
    : "All Courses";

  return (
    <section className="space-y-6">
      <h2 className="text-2xl font-semibold">
        {categoryName}
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {courses?.length ? (
          courses.map((course) => (
            <CourseCard
              key={course.id}
              {...course}
            />
          ))
        ) : (
          <p className="col-span-full text-center text-muted-foreground">
            No courses available yet.
          </p>
        )}
      </div>
    </section>
  );
});

CourseList.displayName = "CourseList";