import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export const HeroSection = () => (
  <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary to-secondary p-12 mb-12 animate-fade-in">
    <div className="relative z-10 max-w-2xl">
      <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
        Ready to stand out from the crowd?
      </h1>
      <p className="text-xl text-white/90 mb-8 max-w-xl">
        Discover courses that will help you achieve your learning goals and unlock your full potential.
      </p>
      <div className="flex gap-4">
        <Button 
          size="lg"
          className="bg-white text-primary hover:bg-gray-100 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 duration-200"
        >
          Get Started
        </Button>
        <Button 
          size="lg"
          variant="outline"
          className="bg-transparent border-white text-white hover:bg-white/10"
        >
          Learn More
        </Button>
      </div>
    </div>
    
    {/* Decorative elements */}
    <div className="absolute bottom-0 right-0 w-64 h-64 bg-yellow-400 rounded-full -mr-32 -mb-32 blur-3xl opacity-20" />
    <div className="absolute top-0 right-0 w-96 h-96 bg-purple-600 rounded-full -mr-48 -mt-48 blur-3xl opacity-20" />
  </section>
);