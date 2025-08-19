import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { memo } from "react";
import { Label } from "@/components/ui/label";

interface SearchFiltersProps {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  difficulty: string;
  setDifficulty: (difficulty: string) => void;
}

const SearchFilters = memo(({ 
  searchQuery, 
  setSearchQuery, 
  difficulty, 
  setDifficulty 
}: SearchFiltersProps) => {
  console.log("SearchFilters component rendering");
  
  return (
    <section 
      className="mb-8 animate-fade-in bg-card rounded-lg p-6 shadow-sm" 
      role="search" 
      aria-label="Course filters"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="search">Search Courses</Label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              id="search"
              placeholder="Search courses..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
              aria-label="Search courses"
            />
          </div>
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="difficulty">Difficulty Level</Label>
          <Select value={difficulty} onValueChange={setDifficulty}>
            <SelectTrigger id="difficulty">
              <SelectValue placeholder="Filter by difficulty" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Levels</SelectItem>
              <SelectItem value="Beginner">Beginner</SelectItem>
              <SelectItem value="Intermediate">Intermediate</SelectItem>
              <SelectItem value="Advanced">Advanced</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </section>
  );
});

SearchFilters.displayName = "SearchFilters";

export default SearchFilters;