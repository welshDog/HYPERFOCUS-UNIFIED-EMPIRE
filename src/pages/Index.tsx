import { useEffect, useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { CourseCard } from "@/components/CourseCard";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";
import { Brain, BookOpen, Share } from "lucide-react";

const Index = () => {
  const [courses, setCourses] = useState([]);
  const { toast } = useToast();

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const { data, error } = await supabase
        .from('courses')
        .select('*')
        .order('rating', { ascending: false })
        .limit(3);

      if (error) throw error;
      setCourses(data);
    } catch (error) {
      console.error('Error fetching courses:', error);
      toast({
        title: "Error",
        description: "Failed to load courses. Please try again later.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      
      <main className="flex-1 p-8">
        <div className="max-w-7xl mx-auto">
          {/* Hero Section */}
          <section className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-primary to-secondary p-8 mb-12 animate-fade-in">
            <div className="relative z-10">
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
                Welcome to Hyperfocus Studios
              </h1>
              <p className="text-xl text-white/90 mb-6 max-w-2xl">
                Unlock your brain's full potential with our innovative courses and brain training exercises.
              </p>
              <button className="bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 duration-200">
                Start Learning
              </button>
            </div>
            <div className="absolute inset-0 bg-black/10" />
          </section>

          {/* Featured Courses */}
          <section className="mb-12 animate-fade-in" style={{ animationDelay: "0.2s" }}>
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">Featured Courses</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses.map((course) => (
                <div key={course.id} style={{ animationDelay: `${0.1}s` }}>
                  <CourseCard {...course} />
                </div>
              ))}
            </div>
          </section>

          {/* Features Grid */}
          <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 animate-fade-in" style={{ animationDelay: "0.4s" }}>
            <div className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
              <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <Brain className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Brain Training</h3>
              <p className="text-gray-600">Enhance your cognitive abilities with scientifically-backed exercises.</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
              <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <BookOpen className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Expert-Led Courses</h3>
              <p className="text-gray-600">Learn from industry experts with our curated course collection.</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
              <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <Share className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Community</h3>
              <p className="text-gray-600">Join a community of learners and share your progress.</p>
            </div>
          </section>

          {/* Community Section */}
          <section className="bg-gradient-to-r from-primary to-secondary rounded-2xl p-8 text-white animate-fade-in" style={{ animationDelay: "0.6s" }}>
            <h2 className="text-2xl font-semibold mb-4">Join Our Learning Community</h2>
            <p className="mb-6">Connect with thousands of students improving their cognitive abilities every day.</p>
            <button className="bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
              Get Started
            </button>
          </section>
        </div>
      </main>
    </div>
  );
};

export default Index;