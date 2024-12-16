import { CourseCard } from "@/components/CourseCard";
import { 
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";

interface FeaturedCoursesProps {
  courses: any[];
  isLoading: boolean;
  currentPage: number;
  totalPages: number;
  setCurrentPage: (page: number) => void;
}

export const FeaturedCourses = ({ 
  courses, 
  isLoading, 
  currentPage, 
  totalPages, 
  setCurrentPage 
}: FeaturedCoursesProps) => (
  <section className="mb-12 animate-fade-in" style={{ animationDelay: "0.2s" }}>
    <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-6">Featured Courses</h2>
    {isLoading ? (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="bg-gray-200 dark:bg-gray-800 rounded-lg h-64" />
          </div>
        ))}
      </div>
    ) : (
      <>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((course) => (
            <div key={course.id} className="animate-fade-in" style={{ animationDelay: `${0.1}s` }}>
              <CourseCard {...course} />
            </div>
          ))}
        </div>
        
        <div className="mt-8">
          <Pagination>
            <PaginationContent>
              <PaginationItem>
                <PaginationPrevious
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                />
              </PaginationItem>
              
              {[...Array(totalPages)].map((_, i) => (
                <PaginationItem key={i + 1}>
                  <PaginationLink
                    onClick={() => setCurrentPage(i + 1)}
                    isActive={currentPage === i + 1}
                  >
                    {i + 1}
                  </PaginationLink>
                </PaginationItem>
              ))}
              
              <PaginationItem>
                <PaginationNext
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </div>
      </>
    )}
  </section>
);