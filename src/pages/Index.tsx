import { Suspense, lazy, memo } from "react";
import { Sidebar } from "@/components/Sidebar";
import { LoadingBrain } from "@/components/LoadingBrain";
import { useCourses } from "@/hooks/useCourses";

// Lazy load components for better initial load performance
const HeroSection = lazy(() => import("@/components/home/HeroSection"));
const SearchFilters = lazy(() => import("@/components/home/SearchFilters"));
const FeaturedCourses = lazy(() => import("@/components/home/FeaturedCourses"));
const FeaturesGrid = lazy(() => import("@/components/home/FeaturesGrid"));
const CommunitySection = lazy(() => import("@/components/home/CommunitySection"));
const AnalyticsDashboard = lazy(() => import("@/components/analytics/AnalyticsDashboard"));

// Memoize static components
const MemoizedSidebar = memo(Sidebar);

const Index = () => {
  console.log("Index component rendering");
  const {
    courses,
    isLoading,
    searchQuery,
    setSearchQuery,
    difficulty,
    setDifficulty,
    currentPage,
    setCurrentPage,
    totalPages
  } = useCourses();

  return (
    <div className="flex min-h-screen bg-background" role="main">
      <MemoizedSidebar />
      
      <main className="flex-1 p-8">
        <div className="max-w-7xl mx-auto space-y-8">
          <Suspense fallback={<LoadingBrain />}>
            <HeroSection />
            
            <SearchFilters
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              difficulty={difficulty}
              setDifficulty={setDifficulty}
            />

            <FeaturedCourses
              courses={courses}
              isLoading={isLoading}
              currentPage={currentPage}
              totalPages={totalPages}
              setCurrentPage={setCurrentPage}
            />

            <AnalyticsDashboard />

            <FeaturesGrid />
            
            <CommunitySection />
          </Suspense>
        </div>
      </main>
    </div>
  );
};

export default Index;