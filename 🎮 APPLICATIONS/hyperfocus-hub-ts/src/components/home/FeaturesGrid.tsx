import { Brain, BookOpen, Users, Target } from "lucide-react";

const FeaturesGrid = () => (
  <section className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12 animate-fade-in" style={{ animationDelay: "0.4s" }}>
    {[
      {
        icon: Brain,
        title: "Expert-Led",
        description: "Learn from industry professionals",
        color: "bg-purple-100 text-purple-600",
      },
      {
        icon: BookOpen,
        title: "Rich Content",
        description: "Access comprehensive materials",
        color: "bg-blue-100 text-blue-600",
      },
      {
        icon: Users,
        title: "Community",
        description: "Connect with fellow learners",
        color: "bg-green-100 text-green-600",
      },
      {
        icon: Target,
        title: "Goal-Oriented",
        description: "Track your progress",
        color: "bg-orange-100 text-orange-600",
      },
    ].map((feature, index) => (
      <div
        key={feature.title}
        className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm hover:shadow-md transition-all duration-300"
      >
        <div className={`h-12 w-12 ${feature.color} rounded-xl flex items-center justify-center mb-4`}>
          <feature.icon className="h-6 w-6" />
        </div>
        <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
        <p className="text-gray-600 dark:text-gray-400">{feature.description}</p>
      </div>
    ))}
  </section>
);

export default FeaturesGrid;