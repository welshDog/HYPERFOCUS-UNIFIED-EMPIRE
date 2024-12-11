import { Sidebar } from "@/components/Sidebar";
import { CourseCard } from "@/components/CourseCard";

const featuredCourses = [
  {
    title: "Memory Mastery",
    description: "Learn techniques to improve your memory and recall abilities.",
    duration: "2h 30m",
    difficulty: "Beginner",
    rating: 4.8,
    imageUrl: "/placeholder.svg",
  },
  {
    title: "Focus Fundamentals",
    description: "Master the art of deep focus and concentration.",
    duration: "1h 45m",
    difficulty: "Intermediate",
    rating: 4.5,
    imageUrl: "/placeholder.svg",
  },
  {
    title: "Speed Reading",
    description: "Double your reading speed while maintaining comprehension.",
    duration: "3h 15m",
    difficulty: "Advanced",
    rating: 4.9,
    imageUrl: "/placeholder.svg",
  },
];

const Index = () => {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      
      <main className="flex-1 p-8">
        <div className="max-w-7xl mx-auto">
          <header className="mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Welcome to Hyperfocus Studios</h1>
            <p className="text-xl text-gray-600">Unlock your brain's full potential with our courses and training.</p>
          </header>

          <section className="mb-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">Featured Courses</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {featuredCourses.map((course) => (
                <CourseCard key={course.title} {...course} />
              ))}
            </div>
          </section>

          <section className="bg-gradient-to-r from-primary to-secondary rounded-lg p-8 text-white">
            <h2 className="text-2xl font-semibold mb-4">Ready to start your journey?</h2>
            <p className="mb-6">Join thousands of students improving their cognitive abilities every day.</p>
            <button className="bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Get Started
            </button>
          </section>
        </div>
      </main>
    </div>
  );
};

export default Index;