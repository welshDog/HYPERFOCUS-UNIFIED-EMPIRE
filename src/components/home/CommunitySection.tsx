import { Button } from "@/components/ui/button";

export const CommunitySection = () => (
  <section className="bg-gradient-to-r from-primary to-secondary rounded-2xl p-8 text-white animate-fade-in" style={{ animationDelay: "0.6s" }}>
    <h2 className="text-2xl font-semibold mb-4">Join Our Learning Community</h2>
    <p className="mb-6">Connect with thousands of students improving their cognitive abilities every day.</p>
    <Button className="bg-white text-primary hover:bg-gray-100 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
      Get Started
    </Button>
  </section>
);