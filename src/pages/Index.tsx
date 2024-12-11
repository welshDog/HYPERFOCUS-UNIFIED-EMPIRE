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
              {featuredCourses.map((course, index) => (
                <div key={course.title} style={{ animationDelay: `${0.1 * (index + 1)}s` }}>
                  <CourseCard {...course} />
                </div>
              ))}
            </div>
          </section>

          {/* Brain Training Section */}
          <section className="bg-white rounded-2xl p-8 shadow-sm mb-12 animate-fade-in" style={{ animationDelay: "0.4s" }}>
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">Daily Brain Training</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-accent/20 rounded-xl p-6 hover:bg-accent/30 transition-all duration-300 transform hover:scale-105 hover:shadow-lg cursor-pointer">
                <h3 className="font-semibold mb-2">Memory Challenge</h3>
                <p className="text-gray-600">Test and improve your memory skills</p>
              </div>
              <div className="bg-accent/20 rounded-xl p-6 hover:bg-accent/30 transition-all duration-300 transform hover:scale-105 hover:shadow-lg cursor-pointer">
                <h3 className="font-semibold mb-2">Focus Timer</h3>
                <p className="text-gray-600">Enhanced concentration exercises</p>
              </div>
              <div className="bg-accent/20 rounded-xl p-6 hover:bg-accent/30 transition-all duration-300 transform hover:scale-105 hover:shadow-lg cursor-pointer">
                <h3 className="font-semibold mb-2">Pattern Recognition</h3>
                <p className="text-gray-600">Boost your cognitive abilities</p>
              </div>
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