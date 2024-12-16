import { Brain, BookOpen, Share } from "lucide-react";

export const FeaturesGrid = () => (
  <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 animate-fade-in" style={{ animationDelay: "0.4s" }}>
    <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
      <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
        <Brain className="h-6 w-6 text-primary" />
      </div>
      <h3 className="text-lg font-semibold mb-2">Brain Training</h3>
      <p className="text-gray-600 dark:text-gray-400">Enhance your cognitive abilities with scientifically-backed exercises.</p>
    </div>
    
    <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
      <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
        <BookOpen className="h-6 w-6 text-primary" />
      </div>
      <h3 className="text-lg font-semibold mb-2">Expert-Led Courses</h3>
      <p className="text-gray-600 dark:text-gray-400">Learn from industry experts with our curated course collection.</p>
    </div>
    
    <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
      <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
        <Share className="h-6 w-6 text-primary" />
      </div>
      <h3 className="text-lg font-semibold mb-2">Community</h3>
      <p className="text-gray-600 dark:text-gray-400">Join a community of learners and share your progress.</p>
    </div>
  </section>
);