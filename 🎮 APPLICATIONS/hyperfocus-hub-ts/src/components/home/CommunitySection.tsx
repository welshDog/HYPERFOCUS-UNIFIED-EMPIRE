import { Button } from "@/components/ui/button";
import { Users } from "lucide-react";

const CommunitySection = () => (
  <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-yellow-400 to-orange-500 p-12 animate-fade-in" style={{ animationDelay: "0.6s" }}>
    <div className="relative z-10">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 bg-white/20 rounded-lg">
          <Users className="h-6 w-6 text-white" />
        </div>
        <h2 className="text-2xl font-semibold text-white">Join Our Learning Community</h2>
      </div>
      <p className="text-lg text-white/90 mb-8 max-w-xl">
        Connect with thousands of students improving their cognitive abilities every day.
        Share experiences, collaborate on projects, and grow together.
      </p>
      <Button 
        size="lg"
        className="bg-white text-orange-500 hover:bg-gray-100 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
      >
        Join Now
      </Button>
    </div>
    
    {/* Decorative elements */}
    <div className="absolute top-0 right-0 w-64 h-64 bg-yellow-300 rounded-full -mr-32 -mt-32 blur-3xl opacity-20" />
    <div className="absolute bottom-0 left-0 w-96 h-96 bg-orange-600 rounded-full -ml-48 -mb-48 blur-3xl opacity-20" />
  </section>
);

export default CommunitySection;