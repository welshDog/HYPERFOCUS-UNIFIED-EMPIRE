import { useState, useEffect, useCallback } from "react";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";

const ITEMS_PER_PAGE = 6;

export const useCourses = () => {
  const [courses, setCourses] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [difficulty, setDifficulty] = useState("all");
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const { toast } = useToast();

  const fetchCourses = useCallback(async () => {
    try {
      setIsLoading(true);
      console.log("Fetching courses with filters:", { searchQuery, difficulty, currentPage });

      let query = supabase
        .from('courses')
        .select('*', { count: 'exact' });

      if (searchQuery) {
        query = query.ilike('title', `%${searchQuery}%`);
      }
      if (difficulty !== 'all') {
        query = query.eq('difficulty', difficulty);
      }

      const from = (currentPage - 1) * ITEMS_PER_PAGE;
      const to = from + ITEMS_PER_PAGE - 1;
      
      const { data, count, error } = await query
        .order('rating', { ascending: false })
        .range(from, to);

      if (error) throw error;

      setCourses(data);
      setTotalPages(Math.ceil((count || 0) / ITEMS_PER_PAGE));
      console.log("Courses fetched successfully:", { count, currentPage, totalPages: Math.ceil((count || 0) / ITEMS_PER_PAGE) });
    } catch (error) {
      console.error('Error fetching courses:', error);
      toast({
        title: "Error",
        description: "Failed to load courses. Please try again later.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  }, [searchQuery, difficulty, currentPage, toast]);

  useEffect(() => {
    fetchCourses();
  }, [fetchCourses]);

  return {
    courses,
    isLoading,
    searchQuery,
    setSearchQuery,
    difficulty,
    setDifficulty,
    currentPage,
    setCurrentPage,
    totalPages
  };
};