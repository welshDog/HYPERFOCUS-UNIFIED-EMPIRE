import { Sidebar } from "@/components/Sidebar";
import { HeroSection } from "@/components/home/HeroSection";
import { SearchFilters } from "@/components/home/SearchFilters";
import { FeaturedCourses } from "@/components/home/FeaturedCourses";
import { FeaturesGrid } from "@/components/home/FeaturesGrid";
import { CommunitySection } from "@/components/home/CommunitySection";
import { AnalyticsDashboard } from "@/components/analytics/AnalyticsDashboard";
import { useCourses } from "@/hooks/useCourses";
import { memo } from "react";

// Memoize static components
const MemoizedSidebar = memo(Sidebar);
const MemoizedHeroSection = memo(HeroSection);
const MemoizedFeaturesGrid = memo(FeaturesGrid);
const MemoizedCommunitySection = memo(CommunitySection);

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
    <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900">
      <MemoizedSidebar />
      
      <main className="flex-1 p-8">
        <div className="max-w-7xl mx-auto">
          <MemoizedHeroSection />
          
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

          <MemoizedFeaturesGrid />
          
          <MemoizedCommunitySection />
        </div>
      </main>
    </div>
  );
};

export default Index;